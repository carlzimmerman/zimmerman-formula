"""CFG881 -- SPARC clump-overfill bound: how much clump-like extra mass can SPARC galaxies hide?
Criteria: FROZEN_CRITERIA.md (f417bc25a, committed alone before this script).
Run: python3 cfg881.py   (CFG881_MUTATE=full|tenth -> separate outputs).  kappa = 1/2 FITTED; nu_e; not theory closed."""
import os, glob, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG881_MUTATE", ""); assert MUT in ("", "full", "tenth"); SUF = f"_MUTATE_{MUT}" if MUT else ""
F_INJ = {"": 0.0, "full": 1.0, "tenth": 0.1}[MUT]; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; RC = 104.0
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
glaw = lambda gb, a0: gb * nu(gb / a0)
J = lambda *p: json.load(open(os.path.join(LANES, *p)))
R870 = J("CFG870_cored_component_joint", "cfg870_results.json"); R877 = J("CFG877_finite_cold_clump", "cfg877_results.json")
Q = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q[v[0]] = dict(inc=float(v[5]), q=int(v[17]), Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9)
        except ValueError: pass

def load():                                    # CFG870's cuts, no mass cut
    gals = []
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        nm = os.path.basename(fn).replace("_rotmod.dat", ""); g = Q.get(nm)
        if not g or g["q"] > 2 or g["inc"] < 30: continue
        pts = []
        for l in open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(t) for t in l.split()[:6]]
            if V <= 0 or R <= 0 or eV / V >= 0.10: continue
            gbar = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
            if gbar <= 0: continue
            pts.append((R, V, eV, gbar, V * V * 1e6 / (R * KPC)))
        if pts:
            a = np.array(pts); gals.append(dict(name=nm, Mb=g["Mb"], R=a[:, 0], V=a[:, 1], eV=a[:, 2], gbar=a[:, 3], gobs=a[:, 4]))
    return gals
GALS = load()

# ---------------- K1: code identity vs CFG877 / CFG870 SPARC D (canonical) ----------------
def D_ident(a0, Vx, Mcl, capped):
    gal = []
    for g in GALS:
        if g["Mb"] > 3e9: continue
        d_ = []
        for R, gbar, go in zip(g["R"], g["gbar"], g["gobs"]):
            gl = float(gbar * nu(gbar / a0)); r = R * 1000 * PC
            if capped: gx = G * min((Vx * 1e3) ** 2 * r ** 3 / (G * (r ** 2 + (RC * PC) ** 2)), Mcl) / (R * KPC) ** 2
            else: gx = (Vx * 1e3) ** 2 * (R * KPC) / ((R * KPC) ** 2 + (RC * PC) ** 2)
            d_.append(math.log10(go / gl) - math.log10((gl + gx) / gl))
        gal.append(float(np.median(d_)))
    return float(np.mean(gal)), len(gal)
a0c = A0["canonical"]; Vxc = R870["canonical"]["Vx"]; Mclc = 81 * (Vxc / math.sqrt(2) * 1e3) ** 4 / (4 * G * a0c)
d877, n877 = D_ident(a0c, Vxc, Mclc, True); d870, n870 = D_ident(a0c, Vxc, None, False)
k1 = [abs(d877 - R877["canonical"]["sparc"]["D"]), abs(d870 - R870["canonical"]["sparc_D"])]
K1 = max(k1) < 1e-9
P("CFG881  SPARC clump-overfill bound" + (f"  [MUTATE {MUT}: inject F_inj = {F_INJ} x M_b per shape]" if MUT else ""))
P(f"  K1 code identity: CFG877 SPARC D |diff| {k1[0]:.1e} (N {n877}), CFG870 T1 D |diff| {k1[1]:.1e} (N {n870}) -> {'PASS' if K1 else 'FAIL'}")

# ---------------- shapes ----------------
SHAPES = ("CORE1", "CORE3", "BARYON", "FLAT")
def shape(g, nm):
    """returns (window mask, a_unit): g_x = M * a_unit (M in Msun; for BARYON M is the fraction F)."""
    R = g["R"]; rk = R * KPC
    if nm == "CORE1": return R <= 3.0, G * Msun * np.minimum(R / 1.0, 1.0) ** 3 / rk ** 2
    if nm == "CORE3": return R <= 6.0, G * Msun * np.minimum(R / 3.0, 1.0) ** 3 / rk ** 2
    if nm == "BARYON": return np.ones_like(R, bool), g["gbar"].copy()
    if nm == "FLAT": return np.ones_like(R, bool), G * Msun * (R / R.max()) / rk ** 2
    raise ValueError(nm)

def bound(gl, gobs, sig, a_unit, gbar, a0, floor=0.10, conv="A", exact=False):
    r = np.log10(gobs / gl); n = len(r); dW = float(np.median(r))
    smed = 1.2533 * max(math.sqrt(float(np.mean(sig ** 2))), float(np.std(r, ddof=1))) / math.sqrt(n)
    sW = math.sqrt(smed ** 2 + floor ** 2); dup = dW if exact else max(dW, 0.0) + 2 * sW
    if conv == "A": stat = lambda M: float(np.median(np.log10(1.0 + M * a_unit / gl)))
    else: stat = lambda M: float(np.median(np.log10(glaw(gbar + M * a_unit, a0) / gl)))
    hi = 1e-30
    while stat(hi) < dup: hi *= 2.0
    lo = 0.0
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if stat(mid) < dup: lo = mid
        else: hi = mid
        if hi - lo <= 1e-14 * hi: break
    return dict(n=n, dW=dW, sW=sW, dup=dup, M=0.5 * (lo + hi), det=bool(dW - 2 * sW > 0))

VARIANTS = (("primary", 0.10, "A"), ("floor0.20", 0.20, "A"), ("convB", 0.10, "B"))
def q(x, p): return float(np.percentile(x, p)) if len(x) else float("nan")
RES = dict(lane="CFG881", mutate=MUT or None, F_inj=F_INJ, K1=k1, K1_pass=K1)
CLS = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]; Vx = R870[foot]["Vx"]; sx = Vx / math.sqrt(2); Mcl = 81 * (sx * 1e3) ** 4 / (4 * G * a0) / Msun
    fb = {"sb7.36": (7.36 / sx) ** 4, "sb8.22": (8.22 / sx) ** 4}
    P(f"\n  [{foot}] a0 {a0:.4e}; sigma_x {sx:.3f} km/s; M_cl = M_block = {Mcl:.3e} Msun; sigma_b variants F x {fb['sb7.36']:.3f} / x {fb['sb8.22']:.3f}")
    rows = {}; k2err = 0.0
    for g in GALS:
        gl = glaw(g["gbar"], a0); sig = 2 * g["eV"] / (g["V"] * math.log(10)); rr = {}
        for sh in SHAPES:
            w, au = shape(g, sh)
            if w.sum() < 3: continue
            go = g["gobs"] + F_INJ * (1.0 if sh == "BARYON" else g["Mb"]) * au     # MUTATE injection (convention A)
            rr[sh] = {}
            for vn, fl, cv in VARIANTS:
                b = bound(gl[w], go[w], sig[w], au[w], g["gbar"][w], a0, fl, cv)
                M = b["M"] * (g["Mb"] if sh == "BARYON" else 1.0); F = M / g["Mb"]
                rr[sh][vn] = dict(n=b["n"], dW=b["dW"], sW=b["sW"], dup=b["dup"], M_max=M, N_max=M / Mcl, F_max=F, det=b["det"])
            if foot == "canonical" and not MUT and g["Mb"] >= 1e9 and sh in ("CORE1", "FLAT"):   # K2 round trip
                Mt = 0.3 * g["Mb"]; gk = gl + Mt * au
                bk = bound(gl[w], gk[w], 0 * sig[w], au[w], g["gbar"][w], a0, 0.0, "A", exact=True)
                k2err = max(k2err, abs(bk["M"] / Mt - 1))
        rows[g["name"]] = dict(Mb=g["Mb"], R_last=float(g["R"].max()), shapes=rr)
    if foot == "canonical" and not MUT:
        RES["K2_max_rel_err"] = k2err; RES["K2_pass"] = k2err < 1e-6
        P(f"  K2 solver round trip (CORE1 + FLAT, M_test = 0.3 M_b, massive): max rel err {k2err:.1e} -> {'PASS' if k2err < 1e-6 else 'FAIL'}")
    summ = {}
    for grp, sel in (("massive", lambda m: m >= 1e9), ("dwarf", lambda m: m < 1e9)):
        summ[grp] = {}
        for sh in SHAPES:
            summ[grp][sh] = {}
            for vn, _, _ in VARIANTS:
                xs = [(r["shapes"][sh][vn], r["Mb"]) for r in rows.values() if sel(r["Mb"]) and sh in r["shapes"]]
                F = np.array([x[0]["F_max"] for x in xs]); N = np.array([x[0]["N_max"] for x in xs])
                summ[grp][sh][vn] = dict(N_gal=len(xs), F_med=q(F, 50), F_p16=q(F, 16), F_p84=q(F, 84),
                                         frac_le_0p1=float(np.mean(F <= 0.1)) if len(F) else float("nan"),
                                         Nmax_med=q(N, 50), Nmax_p16=q(N, 16), Nmax_p84=q(N, 84),
                                         Mmax_med=q(np.array([x[0]["M_max"] for x in xs]), 50),
                                         Mb_med=q(np.array([x[1] for x in xs]), 50),
                                         frac_detected=float(np.mean([x[0]["det"] for x in xs])) if xs else float("nan"),
                                         dW_med=q(np.array([x[0]["dW"] for x in xs]), 50))
    for grp in ("massive", "dwarf"):
        P(f"   {grp} (M_b {'>=' if grp == 'massive' else '<'} 1e9):  shape   N    F_max median [16-84%]   frac<=0.1   N_max median   detected  | floor0.20 med | convB med")
        for sh in SHAPES:
            s = summ[grp][sh]["primary"]; s2 = summ[grp][sh]["floor0.20"]; sb = summ[grp][sh]["convB"]
            P(f"     {sh:7s} {s['N_gal']:4d}   {s['F_med']:8.3f} [{s['F_p16']:.3f}-{s['F_p84']:.3f}]   {s['frac_le_0p1']:5.2f}   {s['Nmax_med']:10.3g}   {s['frac_detected']:5.2f}   | {s2['F_med']:7.3f}  | {sb['F_med']:7.3f}")
    pc = {}
    for sh in SHAPES:
        m = summ["massive"][sh]["primary"]["F_med"]; pc[sh] = "EXCLUDED" if m <= 0.1 else ("ALLOWED" if m >= 1 else "PARTIAL")
    vals = list(pc.values())
    if all(v == "EXCLUDED" for v in vals): cls = "RETENTION EXCLUDED IN BIG GALAXIES"
    elif all(v == "ALLOWED" for v in vals): cls = "RETENTION ALLOWED"
    elif "EXCLUDED" in vals and "ALLOWED" in vals:
        cls = "SHAPE-DEPENDENT (excluded: " + ",".join(k for k, v in pc.items() if v == "EXCLUDED") + "; allowed: " + ",".join(k for k, v in pc.items() if v == "ALLOWED") + ")"
    else: cls = "PARTIAL"
    sbv = {sh: {k: summ["massive"][sh]["primary"]["F_med"] * f for k, f in fb.items()} for sh in SHAPES}
    P("   sigma_b variants (massive median F_max): " + "; ".join(f"{sh} {sbv[sh]['sb7.36']:.3f}/{sbv[sh]['sb8.22']:.3f}" for sh in SHAPES))
    P(f"   per-shape: {pc}")
    P(f"   -> CLASS [{foot}]: {cls}")
    CLS[foot] = cls
    RES[foot] = dict(a0=a0, sigma_x=sx, Mcl_Msun=Mcl, sigma_b_factor=fb, summary=summ, per_shape=pc, sigma_b_variants=sbv, cls=cls, rows=rows)
cc, ca = CLS["canonical"], CLS["alt"]; RES["cls"] = cc if cc == ca else f"{cc} (alt {ca})"
P(f"\n  CLASS: {RES['cls']}")
if MUT:
    ok = all(RES[f]["summary"]["massive"][sh]["primary"]["F_med"] >= 1 for f in ("canonical", "alt") for sh in SHAPES) if MUT == "full" else \
         all(RES[f]["summary"]["massive"][sh]["primary"]["F_med"] > 0.1 for f in ("canonical", "alt") for sh in SHAPES)
    RES["mutate_ok"] = ok; P(f"  MUTATE-{MUT}: {'control behaves as required' if ok else 'CONTROL FAILED'}")
json.dump(RES, open(os.path.join(HERE, f"cfg881_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg881{SUF}.out"), "w").write("\n".join(OUT) + "\n")
