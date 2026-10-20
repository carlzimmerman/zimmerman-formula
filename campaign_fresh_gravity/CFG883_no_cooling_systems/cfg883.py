"""CFG883 -- do systems that never cooled their own gas (globulars, tidal dwarfs, UCDs, collision debris) carry the CFG877
cold clump?  Criteria: FROZEN_CRITERIA.md (986230665, committed alone before this script).
Run: OMP_NUM_THREADS=1 python3 cfg883.py   (CFG883_MUTATE=1 -> clump injected into the data, separate outputs).
kappa = 1/2 FITTED; footings never pooled; not theory closed.  numpy only, one process, about a minute."""
import os, re, csv, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG883_MUTATE", "") == "1"; SUF = "_MUTATE" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ---------------------------------------------------------------- constants (CFG877's)
G, Msun, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
GPC = G * Msun / PC / 1e6                       # pc (km/s)^2 / Msun
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
RC = 104.0                                      # clump core (pc), CFG870
UPS0, SUPS = 1.6, 0.15 * math.log(10)           # GC SPS Upsilon_V and its prior width (ln), CFG332/820
MW_MB = 6.0e10                                  # CFG820's MW baryonic point mass
FLOOR, DIAG, THR, NVULN = 0.05, 9.0, 9.0, 50
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
TRAP = getattr(np, "trapezoid", None) or np.trapz
J = lambda *p: json.load(open(os.path.join(LANES, *p)))

R870 = J("CFG870_cored_component_joint", "cfg870_results.json"); R877 = J("CFG877_finite_cold_clump", "cfg877_results.json")
CL = {}
for f in FOOTS:
    Vx = R870[f]["Vx"]; sx = Vx / math.sqrt(2); Mcl = 81 * (sx * 1e3) ** 4 / (4 * G * A0[f]) / Msun
    CL[f] = dict(Vx=Vx, sx=sx, Mcl=Mcl, rt=GPC * Mcl / Vx ** 2)

def Mx(r_pc, f):                                # clump mass inside r (Msun), CFG877's Mx
    r = np.asarray(r_pc, float); c = CL[f]
    return np.minimum(c["Vx"] ** 2 * r ** 3 / (GPC * (r ** 2 + RC ** 2)), c["Mcl"])

# ---------------------------------------------------------------- Jeans machinery (isotropic, projected)
def king_nu(r, rc, rt):
    z = np.sqrt((1 + (r / rc) ** 2) / (1 + (rt / rc) ** 2)); z = np.clip(z, 1e-12, 1.0)
    return np.where(r < rt, (np.arccos(z) / z - np.sqrt(1 - z * z)) / z ** 2, 0.0)
def king_Lcum(R, rc, rt):                       # King 1962 eq. 18, projected light inside R (arbitrary units)
    x2, xt2 = (R / rc) ** 2, (rt / rc) ** 2
    return np.log1p(x2) - 4 * (np.sqrt(1 + x2) - 1) / np.sqrt(1 + xt2) + x2 / (1 + xt2)
def king_rc_for(rh, rt):
    f = lambda rc: king_Lcum(rh, rc, rt) / king_Lcum(rt, rc, rt) - 0.5
    lo, hi = 1e-5 * rt, 30 * rt          # (first run used 1e3 rt: float cancellation in eq. 18 there; fixed, disclosed)
    if f(lo) < 0 or f(hi) > 0: return None
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if f(mid) > 0: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)

class Tracer:
    def __init__(self, kind, rc=None, rt=None, a=None):
        self.kind = kind
        if kind == "king":
            self.rmax = rt; self.rc = rc; r = np.geomspace(1e-3 * min(rc, rt), rt, 6000); n = king_nu(r, rc, rt)
        else:
            self.rmax = 300 * a; r = np.geomspace(1e-4 * a, self.rmax, 6000); n = (1 + (r / a) ** 2) ** -2.5
        self.r, self.n = r, n
        dm = 4 * np.pi * r ** 2 * n; m = np.concatenate([[4 / 3 * np.pi * r[0] ** 3 * n[0]], 0.5 * (dm[1:] + dm[:-1]) * np.diff(r)])
        m = np.cumsum(m); self.Mstar = m / m[-1]  # unit stellar mass distributed like the tracer
    def _proj(self, R, q):
        out = []
        for Ri in np.atleast_1d(R):
            umax = math.sqrt(max(self.rmax ** 2 - Ri ** 2, 0.0)); x = np.linspace(0, 1, 2001); u = umax * x * x; du = 2 * umax * x
            rr = np.sqrt(Ri ** 2 + u ** 2); out.append(2 * TRAP(np.interp(rr, self.r, q, right=0.0) * du, x))
        return np.array(out)
    def sig2(self, R, Mfun):                     # sigma_los^2 (km/s)^2 at projected R for enclosed mass Mfun(r) [Msun]
        f = self.n * GPC * Mfun(self.r) / self.r ** 2
        seg = 0.5 * (f[1:] + f[:-1]) * np.diff(self.r); Pp = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
        return self._proj(R, Pp) / self._proj(R, self.n)
    def Rh_proj(self):
        Rg = np.geomspace(self.r[0], self.rmax * 0.9999, 600); S = self._proj(Rg, self.n)   # (first run started at 1e-3 rt; fixed)
        c = np.concatenate([[0], np.cumsum(0.5 * (S[1:] * Rg[1:] + S[:-1] * Rg[:-1]) * np.diff(Rg))]); return float(np.interp(0.5 * c[-1], c, Rg))

# ---------------------------------------------------------------- statistic
LU = np.log(UPS0) + np.linspace(-4 * SUPS, 4 * SUPS, 801)
def chi2min(lnobs, eup, elo, s2fun, floor):
    """min over ln Upsilon of sum (ln s_obs - ln s_pred)^2/e^2 + prior; s2fun(Ups[:,None]) -> (nU, nbin) sigma^2."""
    U = np.exp(LU)[:, None]; lp = 0.5 * np.log(np.maximum(s2fun(U), 1e-30))
    e = np.where(lp > lnobs[None, :], eup[None, :], elo[None, :]); e = np.sqrt(e ** 2 + floor ** 2)
    c = (((lnobs[None, :] - lp) / e) ** 2).sum(1) + ((LU - np.log(UPS0)) / SUPS) ** 2
    i = int(np.argmin(c)); return float(c[i]), float(np.exp(LU[i]))
def classify(d):
    if d["n"] >= 3 and d["chiB"] / d["n"] > 3 and d["chiBX"] / d["n"] > 3: return "MODEL INADEQUATE"
    if d["dA"] < DIAG: return "NOT DIAGNOSTIC"
    if d["dchi"] >= THR: return "NO CLUMP"
    if d["dchi"] <= -THR: return "CLUMP PRESENT" + (" (binary-vulnerable)" if d.get("nstar", 1e9) < NVULN else "")
    return "UNDECIDED"
def overall(cls):
    nNC = sum(c == "NO CLUMP" for c in cls); nCPr = sum(c == "CLUMP PRESENT" for c in cls)
    nCPv = sum(c.startswith("CLUMP PRESENT (") for c in cls)
    ndiag = sum(c in ("NO CLUMP", "UNDECIDED") or c.startswith("CLUMP PRESENT") for c in cls)
    if ndiag < 2: k = "NOT DIAGNOSTIC"
    elif nCPr >= 1 and nCPr >= nNC: k = "KILLED"
    elif nCPr >= 1: k = "MIXED"
    elif nNC >= 2: k = "PREDICTION HOLDS" + (" (WEAK)" if nCPv >= nNC else "")
    else: k = "UNDECIDED"
    return dict(cls=k, n_diag=ndiag, n_NC=nNC, n_CP_robust=nCPr, n_CP_vuln=nCPv, n_UND=sum(c == "UNDECIDED" for c in cls))
def lnerr(s, up, lo):
    return math.log((s + up) / s), math.log(s / max(s - lo, 0.1 * s))

P("CFG883  no-atomic-cooling systems vs the CFG877 cold clump" + ("  [MUTATE: clump injected into the data]" if MUT else ""))
RES = dict(lane="CFG883", mutate=MUT, clump={f: CL[f] for f in FOOTS})
for f in FOOTS:
    P(f"  [{f}] V_x {CL[f]['Vx']:.4f} km/s, sigma_x {CL[f]['sx']:.3f} km/s, M_cl {CL[f]['Mcl']:.4e} Msun, cap radius {CL[f]['rt']:.1f} pc")

# ---------------------------------------------------------------- controls K1b, K2
k1b = max(abs(float(Mx(1e9, f)) / R877[f]["Mcl_Msun"] - 1) for f in FOOTS); k1bt = max(abs(CL[f]["rt"] / R877[f]["rt_pc"] - 1) for f in FOOTS)
RES["K1b"] = dict(Mcl_rel=k1b, rt_rel=k1bt, ok=k1b < 1e-9 and k1bt < 1e-6)
P(f"  K1b clump identity vs CFG877 JSON: M_cl rel {k1b:.1e}, r_t rel {k1bt:.1e} -> {'PASS' if RES['K1b']['ok'] else 'FAIL'}")
tp = Tracer("plummer", a=10.0); Rk = np.array([1.0, 10.0, 30.0])
num = tp.sig2(Rk, lambda r: r ** 3 / (r ** 2 + 100.0) ** 1.5); ana = 3 * np.pi * GPC / (64 * 10.0) / np.sqrt(1 + (Rk / 10.0) ** 2)
k2 = float(np.max(np.abs(np.sqrt(num / ana) - 1))); RES["K2"] = dict(maxrel=k2, ok=k2 < 0.01)
P(f"  K2 Jeans vs analytic Plummer (R/a = 0.1, 1, 3): max |sigma ratio - 1| = {k2:.2e} -> {'PASS' if k2 < 0.01 else 'FAIL'}")

# ---------------------------------------------------------------- T1 data
def num1(s):
    s = s.strip()
    if not s or s in ("—", "-"): return None
    if "·" in s:
        a, e = s.split("·"); return float(a.split("+-")[0]) * 10 ** int(e.strip()[2:])
    return float(s.split("+-")[0])
PAR = {}
for l in open(os.path.join(REPO, "real_research", "data", "globular_clusters", "baumgardt_gc_parameters.tsv")):
    if l.startswith("#") or l.startswith("ClusterName"): continue
    c = l.rstrip("\n").split("\t"); nm = re.split(r"\s{2,}", c[0].strip())[0]
    PAR[nm] = dict(Rsun=num1(c[3]), RGC=num1(c[4]), Mass=num1(c[7]), MLV=num1(c[9]), rc=num1(c[10]), rhl=num1(c[11]), rt=num1(c[13]))
BINS = {}
for l in open(os.path.join(REPO, "real_research", "data", "globular_clusters", "baumgardt_gc_veldisp_profiles.tsv")):
    if l.startswith("#") or l.startswith("ClusterName"): continue
    c = l.rstrip("\n").split("\t")
    BINS.setdefault(c[0], []).append(dict(Ras=float(c[1]), N=int(c[2]) if c[2].strip() else 0, s=float(c[3]), up=float(c[4]), lo=float(c[5]), typ=c[6]))

def vc_mw(R_kpc, a0):
    gN = G * MW_MB * Msun / (R_kpc * KPC) ** 2; return math.sqrt(float(gN * nu(gN / a0)) * R_kpc * KPC) / 1e3
def tidal_safe(RGC, f):
    Rp = RGC / 3.0; return CL[f]["sx"] * Rp * 1e3 / vc_mw(Rp, A0[f]) >= math.sqrt(2) * RC

def run_cluster(nm, p, bins, tracer_kind="king", floor=FLOOR, law=False):
    R = np.array([b["Ras"] * p["Rsun"] * 1e3 / 206264.806 for b in bins])
    keep = R < p["rt"]; bins = [b for b, k in zip(bins, keep) if k]; R = R[keep]
    if not len(bins): return None
    if tracer_kind == "king":
        rc = king_rc_for(p["rhl"], p["rt"]); tr = Tracer("king", rc=rc, rt=p["rt"]) if rc else Tracer("plummer", a=p["rhl"]); kind = "king" if rc else "plummer(fallback)"
    else:
        rc = None; tr = Tracer("plummer", a=p["rhl"]); kind = "plummer"
    LV = p["Mass"] / p["MLV"]; kst = tr.sig2(R, lambda r: np.interp(r, tr.r, tr.Mstar))
    out = dict(name=nm, n=len(bins), nstar=sum(b["N"] for b in bins), R_pc=R.tolist(), LV=LV, tracer=kind, rcK=rc, RGC=p["RGC"], foot={})
    for f in FOOTS:
        kx = tr.sig2(R, lambda r: Mx(r, f)); s = np.array([b["s"] for b in bins])
        eu = np.array([lnerr(b["s"], b["up"], b["lo"])[0] for b in bins]); el = np.array([lnerr(b["s"], b["up"], b["lo"])[1] for b in bins])
        if MUT:
            s_new = np.sqrt(s ** 2 + kx); s = s_new                     # proportional errors kept (ln errors unchanged)
        lnobs = np.log(s)
        if law:
            a0 = A0[f]; r12 = 4 / 3 * p["rhl"] * PC; yext = G * MW_MB * Msun / (p["RGC"] * KPC) ** 2 / a0
            B = lambda U: nu(G * (U * LV * Msun / 2) / r12 ** 2 / a0 + yext)
            sB = lambda U: U * LV * kst[None, :] * B(U); sBX = lambda U: U * LV * kst[None, :] * B(U) + kx[None, :]
            base0 = np.sqrt(UPS0 * LV * kst * float(B(UPS0)))
        else:
            sB = lambda U: U * LV * kst[None, :]; sBX = lambda U: U * LV * kst[None, :] + kx[None, :]; base0 = np.sqrt(UPS0 * LV * kst)
        cB, uB = chi2min(lnobs, eu, el, sB, floor); cBX, uBX = chi2min(lnobs, eu, el, sBX, floor)
        cA, _ = chi2min(np.log(base0), eu, el, sBX, floor); cA0, _ = chi2min(np.log(base0), eu, el, sB, floor)
        ex = np.sqrt(kx); m = ex > s; ee = np.sqrt(eu ** 2 + floor ** 2)
        cfl = float((((np.log(s) - np.log(ex)) / ee) ** 2 * m).sum())
        d = dict(chiB=cB, chiBX=cBX, dchi=cBX - cB, dA=cA - cA0, upsB=uB, upsBX=uBX, n=len(bins), nstar=out["nstar"],
                 s_obs=s.tolist(), s_B=base0.tolist(), s_x=ex.tolist(), floor_chi2=cfl, safe=tidal_safe(p["RGC"], f))
        d["cls"] = classify(d); out["foot"][f] = d
    return out

def t1(label, tracer_kind="king", floor=FLOOR, law=False, types=("RV",), tidal=True, verbose=False):
    rows, skipped = [], []
    for nm, bl in sorted(BINS.items()):
        if nm == "NGC 6715" or nm not in PAR: skipped.append(nm); continue
        b = [x for x in bl if types is None or x["typ"] in types]
        if not b: continue
        r = run_cluster(nm, PAR[nm], b, tracer_kind, floor, law)
        if r is None: skipped.append(nm + " (all bins beyond rt)"); continue
        rows.append(r)
    res = dict(label=label, N_all=len(rows), skipped=skipped, foot={})
    for f in FOOTS:
        sub = [r for r in rows if (r["foot"][f]["safe"] or not tidal)]
        cls = [r["foot"][f]["cls"] for r in sub]; ov = overall(cls)
        ov["N"] = len(sub); ov["sum_dchi_diag"] = float(sum(r["foot"][f]["dchi"] for r in sub if r["foot"][f]["cls"] not in ("NOT DIAGNOSTIC", "MODEL INADEQUATE")))
        ov["NC"] = [r["name"] for r in sub if r["foot"][f]["cls"] == "NO CLUMP"]
        ov["CP"] = [r["name"] + ("*" if "vuln" in r["foot"][f]["cls"] else "") for r in sub if r["foot"][f]["cls"].startswith("CLUMP PRESENT")]
        ov["UND"] = [r["name"] for r in sub if r["foot"][f]["cls"] == "UNDECIDED"]
        ov["INAD"] = [r["name"] for r in sub if r["foot"][f]["cls"] == "MODEL INADEQUATE"]
        res["foot"][f] = ov
    return rows, res

P("\n=== T1 PRIMARY: globular-cluster RV sigma profiles, King tracer, Newton baseline, tidally safe clusters")
rows1, res1 = t1("primary")
kings = [r for r in rows1 if r["tracer"] == "king"]; fb = [r["name"] for r in rows1 if r["tracer"] != "king"]
k3 = []
for r in kings:
    tr = Tracer("king", rc=r["rcK"], rt=PAR[r["name"]]["rt"]); k3.append(abs(tr.Rh_proj() / PAR[r["name"]]["rhl"] - 1))
RES["K3"] = dict(maxrel=float(max(k3)), N=len(k3), fallback=fb, ok=max(k3) < 0.01)
P(f"  K3 King solver: projected R_h = rh_l to max rel {max(k3):.2e} over {len(k3)} clusters -> {'PASS' if max(k3) < 0.01 else 'FAIL'}; Plummer fallbacks {len(fb)}: {fb}")
P(f"  clusters with RV bins: {res1['N_all']} (skipped: {res1['skipped']})")
for f in FOOTS:
    P(f"\n  [{f}] tidally safe clusters scored: {res1['foot'][f]['N']}")
    P(f"    {'cluster':12s} {'R_GC':>6s} {'bins':>4s} {'N*':>5s} {'R_max':>6s} {'s_obs(out)':>10s} {'Newton':>7s} {'clump':>6s} {'dchi2_A':>8s} {'dchi2':>8s} {'floor':>6s}  class")
    for r in sorted(rows1, key=lambda q: -q["foot"][f]["dA"]):
        d = r["foot"][f]
        if not d["safe"]: continue
        i = int(np.argmax(r["R_pc"]))
        if d["dA"] >= 1 or d["cls"] not in ("NOT DIAGNOSTIC",):
            P(f"    {r['name']:12s} {r['RGC']:6.1f} {r['n']:4d} {r['nstar']:5d} {r['R_pc'][i]:6.1f} {d['s_obs'][i]:10.2f} {d['s_B'][i]:7.2f} {d['s_x'][i]:6.2f} {d['dA']:8.1f} {d['dchi']:+8.1f} {d['floor_chi2']:6.1f}  {d['cls']}")
    nd = sum(1 for r in rows1 if r["foot"][f]["safe"] and r["foot"][f]["dA"] < 1)
    P(f"    (+ {nd} tidally safe clusters with dchi2_A < 1 not listed)")
    o = res1["foot"][f]
    P(f"    -> OVERALL {o['cls']}: diagnostic {o['n_diag']}, NO CLUMP {o['n_NC']} {o['NC']}, CLUMP PRESENT robust {o['n_CP_robust']} / binary-vulnerable {o['n_CP_vuln']} {o['CP']}, UNDECIDED {o['UND']}, inadequate {o['INAD']}; sum dchi2 (diagnostic) {o['sum_dchi_diag']:+.1f}")
RES["T1"] = dict(summary=res1, rows=rows1)
# Pal 14 is the one cluster the King solver cannot match (R_h/rt = 0.60 > 0.454, the King maximum) -> Plummer per the criteria.
# Sensitivity (reported): the most extended TRUNCATED King (rc = 30 rt), which keeps every star inside rt.
p14 = PAR["Pal 14"]; b14 = [x for x in BINS["Pal 14"] if x["typ"] == "RV"]; R14 = np.array([b["Ras"] * p14["Rsun"] * 1e3 / 206264.806 for b in b14])
tr14 = Tracer("king", rc=30 * p14["rt"], rt=p14["rt"]); LV14 = p14["Mass"] / p14["MLV"]
kst14 = tr14.sig2(R14, lambda r: np.interp(r, tr14.r, tr14.Mstar)); s14 = np.array([b["s"] for b in b14])
eu14 = np.array([lnerr(b["s"], b["up"], b["lo"])[0] for b in b14]); el14 = np.array([lnerr(b["s"], b["up"], b["lo"])[1] for b in b14])
RES["Pal14_truncated_king"] = {}
for f in FOOTS:
    kx14 = tr14.sig2(R14, lambda r: Mx(r, f)); so14 = np.sqrt(s14 ** 2 + kx14) if MUT else s14
    cB, _ = chi2min(np.log(so14), eu14, el14, lambda U: U * LV14 * kst14[None, :], FLOOR); cBX, _ = chi2min(np.log(so14), eu14, el14, lambda U: U * LV14 * kst14[None, :] + kx14[None, :], FLOOR)
    b0 = np.log(np.sqrt(UPS0 * LV14 * kst14)); cA, _ = chi2min(b0, eu14, el14, lambda U: U * LV14 * kst14[None, :] + kx14[None, :], FLOOR); cA0, _ = chi2min(b0, eu14, el14, lambda U: U * LV14 * kst14[None, :], FLOOR)
    d = dict(n=1, chiB=cB, chiBX=cBX, dchi=cBX - cB, dA=cA - cA0, nstar=16, s_x=float(np.sqrt(kx14[0])), s_B=float(np.exp(b0[0]))); d["cls"] = classify(d); RES["Pal14_truncated_king"][f] = d
    P(f"  Pal 14 sensitivity [{f}]: truncated King rc = 30 rt (R_h 0.454 rt): Newton {d['s_B']:.2f}, clump term {d['s_x']:.2f}, dchi2_A {d['dA']:.1f}, dchi2 {d['dchi']:+.1f} -> {d['cls']}")

P("\n=== T1 variants (reported, not deciding)")
VAR = {}
for lab, kw in (("all R_GC (no tidal cut)", dict(tidal=False)), ("all bin types", dict(types=None)), ("floor 0.10", dict(floor=0.10)),
                ("Plummer tracer", dict(tracer_kind="plummer")), ("law+EFE baseline", dict(law=True))):
    _, rv = t1(lab, **kw); VAR[lab] = rv["foot"]
    for f in FOOTS:
        o = rv["foot"][f]
        P(f"  {lab:24s} [{f:9s}] N {o['N']:3d}: {o['cls']:24s} diag {o['n_diag']:2d}, NC {o['n_NC']:2d}, CP robust {o['n_CP_robust']} {o['CP']}, UND {o['n_UND']}, inad {len(o['INAD'])}")
RES["T1_variants"] = VAR

# ---------------------------------------------------------------- T2: CFG332 four, Wolf (CFG820 estimator)
P("\n=== T2 SECONDARY: CFG332's four outer-halo globulars, global sigma (Wolf; CFG820's estimator)")
GC = J("CFG332_globulars_three_routes", "cfg332_globulars_results.json")["clusters"]
def wolf2(M, rhl, boost=1.0): return GPC * boost * M / (6.0 * (4.0 / 3.0) * rhl)
c820 = {}
for l in open(os.path.join(LANES, "CFG820_stiffness_from_globulars", "cfg820.out")):
    m = re.match(r"\s+(.+?)\s*: sigma_obs .*?Newton ([0-9.]+);", l)
    if m: c820[m.group(1).strip()] = float(m.group(2))
k1 = max(abs(math.sqrt(wolf2(UPS0 * g["LV"], g["rhl"])) - c820[g["name"]]) for g in GC)
RES["K1"] = dict(maxdiff=k1, ok=k1 < 0.005 and len(c820) == 4)
P(f"  K1 Newton sigma vs CFG820's printed values: max |diff| {k1:.4f} km/s over {len(c820)} clusters -> {'PASS' if RES['K1']['ok'] else 'FAIL'}")
T2 = {}
for f in FOOTS:
    a0 = A0[f]; T2[f] = {}
    for g in GC:
        r12 = 4 / 3 * g["rhl"]; sx2 = float(GPC * Mx(r12, f) / (3 * r12)); s = g["so"]; e = g["eso"] / g["so"]
        if MUT: s = math.sqrt(s ** 2 + sx2)
        lo = np.array([math.log(s)]); ee = np.array([e])
        yext = G * MW_MB * Msun / (g["RGC"] * KPC) ** 2 / a0
        for base in ("Newton", "law+EFE"):
            if base == "Newton": sB = lambda U: wolf2(U * g["LV"], g["rhl"]) * np.ones((1, 1))
            else: sB = lambda U: wolf2(U * g["LV"], g["rhl"], nu(G * (U * g["LV"] * Msun / 2) / (r12 * PC) ** 2 / a0 + yext))
            sBX = lambda U: sB(U) + sx2
            cB, _ = chi2min(lo, ee, ee, sB, 0.0); cBX, _ = chi2min(lo, ee, ee, sBX, 0.0)
            b0 = math.sqrt(float(np.squeeze(sB(np.array([[UPS0]])))))
            cA, _ = chi2min(np.array([math.log(b0)]), ee, ee, sBX, 0.0); cA0, _ = chi2min(np.array([math.log(b0)]), ee, ee, sB, 0.0)
            d = dict(n=1, chiB=cB, chiBX=cBX, dchi=cBX - cB, dA=cA - cA0, nstar=g["N"], s_obs=s, s_B=b0, s_x=math.sqrt(sx2))
            d["cls"] = classify(d); T2[f][f"{g['name']}|{base}"] = d
            P(f"  [{f:9s}] {g['name']:9s} {base:8s}: sigma_obs {s:.2f}+-{g['eso']:.2f}  base {b0:.2f}  clump term {math.sqrt(sx2):.2f}  base+clump {math.sqrt(b0**2+sx2):.2f}  dchi2_A {d['dA']:6.1f}  dchi2 {d['dchi']:+6.1f}  {d['cls']}")
RES["T2"] = T2

# ---------------------------------------------------------------- T3: non-globular systems
P("\n=== T3 non-globular systems: diagnostic power first")
T3 = {}
P("  T3a Lelli+2015 tidal dwarfs (V_c at R_out; Newton baseline, class E)")
for row in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))):
    nm = row["object"]; R = float(row["R_out_kpc"]) * 1e3; Mb = float(row["M_bar_1e8"]) * 1e8; eMb = float(row["e_M_bar_1e8"]) * 1e8
    V, eV = float(row["V_circ_kms"]), float(row["e_V_circ_kms"])
    for f in FOOTS:
        VN = math.sqrt(GPC * Mb / R); eVN = 0.5 * VN * eMb / Mb; VX2 = float(GPC * Mx(R, f) / R)
        Vo = math.sqrt(V ** 2 + VX2) if MUT else V; ee = math.sqrt(eV ** 2 + eVN ** 2)
        VBX = math.sqrt(VN ** 2 + VX2); dA = ((VBX - VN) / ee) ** 2; dchi = ((Vo - VBX) ** 2 - (Vo - VN) ** 2) / ee ** 2
        gN = GPC * Mb / R ** 2 * 1e6 / PC; Vlaw = math.sqrt(float(gN * nu(gN / A0[f])) * R * PC) / 1e3
        d = dict(n=1, chiB=0, chiBX=0, dA=dA, dchi=dchi, V_obs=Vo, eV=eV, V_N=VN, V_x=math.sqrt(VX2), V_law_iso=Vlaw); d["cls"] = classify(d)
        T3[f"TDG {nm}|{f}"] = d
        P(f"    [{f:9s}] {nm:11s} R_out {R/1e3:4.1f} kpc  V_obs {Vo:5.1f}+-{eV:.0f}  Newton {VN:5.1f}  clump V_x {math.sqrt(VX2):4.2f}  (law iso {Vlaw:5.1f})  dchi2_A {dA:.1e}  {d['cls']}")
P("  T3b LVD compact objects beyond the LG (Wolf; Upsilon_V 2 +- 0.15 dex; 20% sigma error where missing)")
for row in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_local_field_distant.csv"))):
    try: s = float(row["vlos_sigma"])
    except ValueError: continue
    if math.isnan(s) or row["name"] == "KDG 64": continue
    nm = row["name"]; rh = float(row["rhalf_sph_physical"] or row["rhalf_physical"]); r12 = 4 / 3 * rh; L = 10 ** (0.4 * (4.83 - float(row["M_V"])))
    try: em, ep = float(row["vlos_sigma_em"]), float(row["vlos_sigma_ep"]); miss = math.isnan(em) or math.isnan(ep)
    except ValueError: miss = True
    if miss: em = ep = 0.2 * s
    for f in FOOTS:
        sx2 = float(GPC * Mx(r12, f) / (3 * r12)); so = math.sqrt(s ** 2 + sx2) if MUT else s
        eu, el = lnerr(so, ep * so / s, em * so / s); lo = np.array([math.log(so)])
        sB = lambda U: GPC * (U * 2 / 1.6) * L / (6 * r12) * np.ones((1, 1))   # Upsilon_V = 2 centred: U/1.6 rescales the GC prior centre
        sBX = lambda U: sB(U) + sx2
        cB, _ = chi2min(lo, np.array([eu]), np.array([el]), sB, 0.0); cBX, _ = chi2min(lo, np.array([eu]), np.array([el]), sBX, 0.0)
        b0 = math.sqrt(GPC * 2 * L / (6 * r12)); la = np.array([math.log(b0)])
        cA, _ = chi2min(la, np.array([eu]), np.array([el]), sBX, 0.0); cA0, _ = chi2min(la, np.array([eu]), np.array([el]), sB, 0.0)
        gN = GPC * L / r12 ** 2 * 1e6 / PC; slaw = b0 * math.sqrt(float(nu(gN / A0[f])))
        d = dict(n=1, chiB=cB, chiBX=cBX, dchi=cBX - cB, dA=cA - cA0, s_obs=so, s_B=b0, s_x=math.sqrt(sx2), s_law=slaw, r12=r12, err_missing=miss, host=row["host"])
        d["cls"] = classify(d) + (" [class unknown: reported only]" if nm == "Fluffy" else ""); T3[f"LVD {nm}|{f}"] = d
        P(f"    [{f:9s}] {nm:9s} ({row['host']}) r12 {r12:5.1f} pc  M_V {float(row['M_V']):6.2f}  sigma {so:5.2f}{' (err 20%)' if miss else ''}  Newton {b0:5.2f}  law {slaw:5.2f}  clump term {math.sqrt(sx2):4.2f}  dchi2_A {d['dA']:.2f}  dchi2 {d['dchi']:+.2f}  {d['cls']}")
P("  T3c NGC 1052 trail (CFG655's frozen inputs; Newton baseline = label E, external label)")
TRAIL = {"DF2": dict(Ms=2.0e8, eMs=0.20, Re=2.0, obs=(8.5, 2.3, 3.1)), "DF4": dict(Ms=1.5e8, eMs=0.27, Re=1.6, obs=(6.3, 2.5, 1.6)),
         "DF9": dict(Ms=1.4e8, eMs=0.23, Re=1.1, obs=(6.5, 3.9, 4.3))}   # copied from cfg655_trail_supply.py GAL (primary distances)
for nm, g in TRAIL.items():
    r12 = 4 / 3 * g["Re"] * 1e3
    for f in FOOTS:
        sN = math.sqrt(GPC * g["Ms"] / (6 * r12)); eN = abs(math.sqrt(GPC * g["Ms"] * (1 + g["eMs"]) / (6 * r12)) - sN)
        sx2 = float(GPC * Mx(r12, f) / (3 * r12)); sBX = math.sqrt(sN ** 2 + sx2); so, up, lo = g["obs"]
        if MUT: so = math.sqrt(so ** 2 + sx2)
        e = lambda sp: math.sqrt((up if sp > so else lo) ** 2 + eN ** 2)
        dchi = ((so - sBX) / e(sBX)) ** 2 - ((so - sN) / e(sN)) ** 2; dA = ((sBX - sN) / math.sqrt(up ** 2 + eN ** 2)) ** 2
        d = dict(n=1, chiB=0, chiBX=0, dA=dA, dchi=dchi, s_obs=so, s_N=sN, s_x=math.sqrt(sx2)); d["cls"] = classify(d); T3[f"trail {nm}|{f}"] = d
        P(f"    [{f:9s}] {nm}  r12 {r12/1e3:.2f} kpc  sigma {so:.2f}  Newton {sN:.2f}  clump term {math.sqrt(sx2):.2f}  base+clump {sBX:.2f}  dchi2_A {dA:.3f}  {d['cls']}")
RES["T3"] = T3
t3diag = [k for k, v in T3.items() if not v["cls"].startswith("NOT DIAGNOSTIC")]
P(f"  T3 diagnostic systems: {t3diag if t3diag else 'none'}")

# ---------------------------------------------------------------- verdict
cc, ca = res1["foot"]["canonical"]["cls"], res1["foot"]["alt"]["cls"]
order = ["KILLED", "MIXED", "UNDECIDED", "NOT DIAGNOSTIC", "PREDICTION HOLDS (WEAK)", "PREDICTION HOLDS"]
head = cc if cc == ca else (min((cc, ca), key=order.index) + f" (canonical {cc}; alt {ca})")
RES["cls"] = head
P(f"\n  CLASS (T1 primary): {head}")
P(f"  controls: K1 {'PASS' if RES['K1']['ok'] else 'FAIL'}, K1b {'PASS' if RES['K1b']['ok'] else 'FAIL'}, K2 {'PASS' if RES['K2']['ok'] else 'FAIL'}, K3 {'PASS' if RES['K3']['ok'] else 'FAIL'}")
if MUT:
    okf = []
    for f in FOOTS:
        sub = [r["foot"][f] for r in rows1 if r["foot"][f]["safe"] and r["foot"][f]["cls"] not in ("NOT DIAGNOSTIC", "MODEL INADEQUATE")]
        frac = sum(d["cls"].startswith("CLUMP PRESENT") for d in sub) / max(len(sub), 1)
        okf.append(frac >= 0.8 and res1["foot"][f]["cls"] == "KILLED"); P(f"  MUTATE [{f}]: CLUMP PRESENT in {frac:.0%} of {len(sub)} diagnostic clusters; overall {res1['foot'][f]['cls']}")
    ok3 = not t3diag or all("Fluffy" in k for k in t3diag)
    RES["mutate_ok"] = all(okf) and ok3
    P(f"  MUTATE: {'control behaves as required' if RES['mutate_ok'] else 'CONTROL FAILED'} (T3 stays not diagnostic: {ok3})")
json.dump(RES, open(os.path.join(HERE, f"cfg883_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg883{SUF}.out"), "w").write("\n".join(OUT) + "\n")
