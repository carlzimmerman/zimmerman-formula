#!/usr/bin/env python3
"""MK2 rows a1, b, c, d, g, h and the trade-off check (criteria 3b4f515ff8, amendment A1 5f2304176e), with KA1-KA4 (rows c, d, g,
B1a parts), KA2, KA3; MUTATE M-NOCAP, M-NOSELF, M-2X on rows c and d (separate outputs).
    python3 mk2_rows.py  -> mk2_rows.json / .out, mk2_rows_MUTATE.json / .out   (preemptible: per-arm parts in parts/rows/)
Read-only inputs: kd1.json; QX2's qx2.py (X-COP builder, gate, psi_profile); QX5's groups(); X-COP FITS profiles; one1.json.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import mk2_lib as L
from astropy.io import fits
PARTS = os.path.join(HERE, "parts", "rows"); os.makedirs(PARTS, exist_ok=True)
OUT, OUTM = [], []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
def PM(s=""): print("[MUTATE] " + s, flush=True); OUTM.append(str(s))
G, MS, KPC, MPC, C = L.G, L.MSUN, L.KPC, L.MPC, L.C_SI
CL6 = os.path.join(REPO, "closure_2026_11_06")
KD1 = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
ONE = json.load(open(os.path.join(REPO, "fable52_push", "ONE1_counted_once", "one1.json")))
XP = {f: float(ONE["foot"][f]["X"]) for f in L.FOOT}
I0 = {f: KD1["footings"][f]["setting"]["I0_Mpc-2"] for f in L.FOOT}
RHO = {f: I0[f] * C ** 2 / (8 * math.pi * G) / MPC ** 2 for f in L.FOOT}           # today's mean cold density [kg/m^3]
N0 = {f: I0[f] / 2 for f in L.FOOT}                                                 # n0 = 4 pi G rho / c^2 [Mpc^-2]
CS = 10 ** (4.0 - 0.025 * np.arange(121))                                           # 1e4 .. 10 km/s, descending (the frozen grid)
XCL = 5.41
RES = dict(lane="MK2", file="mk2_rows", criteria="3b4f515ff8 (A1 5f2304176e)", note=L.NOTE, KA={}, rows={}, cs_grid=CS.tolist())
def xT(cs): return (cs * 1e3 / C) ** 2
P(f"MK2 rows. rho_bar_d today {RHO['canonical']:.4e} / {RHO['alt']:.4e} kg/m^3; n0 {N0['canonical']:.4e} Mpc^-2. {L.NOTE}")

# ============================================================== row a1: KD1 B1a with w = x_T / (1 + xbar - x_T), xbar(z) = 3 x_T ln(1+z) (clock zero today)
P("\nROW a1 (KD1 B1a: w(z 3400) <= 0.01)")
def w_exp(x_T, z): xb = 3 * x_T * math.log(1 + z); return x_T / (1 + xb - x_T)
lo, hi = 1e-8, 0.3
for _ in range(200):
    mid = math.sqrt(lo * hi); lo, hi = (mid, hi) if w_exp(mid, 3400) <= 0.01 else (lo, mid)
csa1 = C * math.sqrt(lo) / 1e3
RES["rows"]["a1"] = dict(cs_max_kms=csa1, xT_max=lo, w_at_500=w_exp(xT(500), 3400), BBN="no stiff phase: w = x_T at every epoch (KD1 B1b passes for every c_s)")
P(f"  w(z 3400) <= 0.01 holds for x_T <= {lo:.5f}, i.e. c_s <= {csa1:.0f} km/s (both footings). At 500 km/s w = {w_exp(xT(500), 3400):.3e}. B1b (BBN): no stiff phase, passes.")
for f in L.FOOT:
    a = 1 / 3401.0; mu = math.sqrt(I0[f] * 0.99 / (4 * 0.01 * a ** 3)); ref = KD1["footings"][f]["B1"]["mu_B1a"]
    RES["KA"][f"KA1 B1a quadratic {f}"] = dict(value=mu, ref=ref, ok=bool(abs(mu / ref - 1) <= 1e-6))
    P(f"  KA1 [{f}] the quadratic's B1a line through the same w code: {mu:.3f} (KD1 {ref:.3f}) -> {'PASS' if abs(mu / ref - 1) <= 1e-6 else 'FAIL'}")

# ============================================================== row b: the clustering lines (not carried; table reported)
P("\nROW b clustering scale: comoving Jeans wavenumber sqrt(n0 (1+z) / x_T) [1/Mpc]")
tab = {}
for cs in (30, 50, 100, 150, 200, 300, 500, 700, 1000):
    row = {z: math.sqrt(N0["canonical"] * (1 + z) / xT(cs)) for z in (0, 2, 5, 30, 1100, 3400)}; tab[cs] = row
    P(f"  c_s {cs:5d} km/s: " + ", ".join(f"z {z}: {v:.3g}" for z, v in row.items()) + f"  (Jeans length today {2 * math.pi / row[0]:.0f} Mpc comoving)")
dem = dict(cmb_lensing=C / 1e3 * math.sqrt(N0["canonical"] / 1.0 ** 2), growth=C / 1e3 * math.sqrt(N0["canonical"] / (0.2 * 0.674) ** 2),
           forest=C / 1e3 * math.sqrt(3 * N0["canonical"] / (3 * 0.674) ** 2))
RES["rows"]["b"] = dict(table=tab, lines={
    "KD1 G9a / QX3 G2 (CMB-lensing Jeans line)": dict(status="NOT CARRIED", presupposes="the dust builds the late-time lensing structure as the cold reference does (galaxies and groups sit in dust halos)",
                                                     would_demand_cs_max_kms=dem["cmb_lensing"], how="comoving k_J >= 1 /Mpc at z = 0 (L <= 400 kernel, stand-in, reported only)"),
    "growth stand-in (k <= 0.2 h/Mpc)": dict(status="NOT CARRIED", presupposes="the dust supplies the linear growth on those scales", would_demand_cs_max_kms=dem["growth"]),
    "forest stand-in (k <= 3 h/Mpc at z 2)": dict(status="NOT CARRIED", presupposes="the dust supplies small-scale power at z 2-4", would_demand_cs_max_kms=dem["forest"])})
for k, v in RES["rows"]["b"]["lines"].items():
    P(f"  {k}: NOT CARRIED (presupposes {v['presupposes']}); if carried it would demand c_s <= {v['would_demand_cs_max_kms']:.0f} km/s (stand-in, not graded)")

# ============================================================== trade-off numeric check (section 2)
P("\nTRADE-OFF check (section 2): k 20 /Mpc physical, background from z 2 to 5 (n 27 -> 216 x n0)")
TO = {}
for name, nf, nprime, ninv in (("exponential c_s 5 km/s", lambda x: N0["canonical"] * math.exp(x / xT(5)), lambda x: N0["canonical"] * math.exp(x / xT(5)) / xT(5), lambda n: xT(5) * math.log(n / N0["canonical"])),
                                ("exponential c_s 500 km/s", lambda x: N0["canonical"] * math.exp(x / xT(500)), lambda x: N0["canonical"] * math.exp(x / xT(500)) / xT(500), lambda n: xT(500) * math.log(n / N0["canonical"])),
                                ("quadratic mu 198", lambda x: 198.25 ** 2 * x, lambda x: 198.25 ** 2, lambda n: n / 198.25 ** 2)):
    na, nb = 27 * N0["canonical"], 216 * N0["canonical"]; xa, xb, x0 = ninv(na), ninv(nb), ninv(N0["canonical"]); k2 = 400.0
    hyp = min(nprime(xa + t * (xb - xa)) for t in np.linspace(0, 1, 201)) >= k2
    width = xb - xa; bound = (nb - na) / k2; thr = (xa - x0) + bound
    def lg(x):   # log10(n(x) / n0), overflow-safe
        try: return math.log10(nf(x) / N0["canonical"])
        except OverflowError: return (x / xT(5) if "c_s 5 " in name else x / xT(500)) / math.log(10)
    floods = {d: lg(x0 + d) for d in (1e-7, 4e-6, 3e-5)}
    TO[name] = dict(hypothesis_holds=bool(hyp), width=width, bound=bound, width_le_bound=bool(width <= bound * (1 + 1e-12)), threshold=thr,
                    wells_log10_n_over_n0={str(k): v for k, v in floods.items()}, consistent=bool((not hyp) or (width <= bound and all(v >= math.log10(216) for d, v in floods.items() if d >= thr))))
    P(f"  {name}: n' >= k^2 on the stretch: {hyp}; width {width:.3e} vs (n_b - n_a)/k^2 {bound:.3e}; flooding threshold {thr:.3e}; wells 1e-7 / 4e-6 / 3e-5 hold log10(n/n0) = "
      + " / ".join(f"{v:.3g}" for v in floods.values()) + f" -> theorem {'applies and holds' if hyp and TO[name]['consistent'] else ('does not apply (not cold at k 20)' if not hyp else 'VIOLATED')}")
avg_slope = (27 - 1) * N0["canonical"] / (4e-6 - (216 - 27) * N0["canonical"] / 400)
TO["DT1 derived claim"] = dict(avg_slope_max=avg_slope, jeans_length_Mpc_somewhere=2 * math.pi / math.sqrt(avg_slope),
                               reading="average slope of n over [xbar_0, x_a] <= this, so n' <= it at SOME offset in the stretch (mean value), not at every one")
P(f"  DT1's 'slope <= 0.14 per Mpc^2, Jeans length >= 17 Mpc for z < 2': the theorem gives an AVERAGE slope <= {avg_slope:.3f} over z 0-2, so a Jeans length >= {2 * math.pi / math.sqrt(avg_slope):.1f} Mpc at some epoch of the stretch, not at every one.")
RES["rows"]["tradeoff"] = TO

# ============================================================== X-COP and groups: builders
q2src = open(os.path.join(CL6, "QX2_clusters", "qx2.py")).read()
Q2 = dict(__file__=os.path.join(CL6, "QX2_clusters", "qx2.py"), __name__="qx2_prefix"); _argv = sys.argv; sys.argv = [sys.argv[0]]
exec(compile(q2src[:q2src.index("# ---------- iter 1: plain law ----------")], "qx2.py", "exec"), Q2); sys.argv = _argv
exec(compile(q2src[q2src.index("def psi_profile(c):"):q2src.index("for c in XC:\n    rr, psi = psi_profile(c)")], "qx2.py:psi_profile", "exec"), Q2)
XC, gateQ2, A0Q = Q2["XC"], Q2["gate"], Q2["A0"]
XD = os.path.join(REPO, "real_research", "data", "xcop")
def ll(x, y, t, rfar):
    if t <= x[0]: return y[0] * (t / x[0]) ** 3
    if t >= x[-1]:
        sl = (math.log(y[-1]) - math.log(y[-4])) / (math.log(x[-1]) - math.log(x[-4])); return y[-1] * (min(t, rfar) / x[-1]) ** sl
    return math.exp(np.interp(math.log(t), np.log(x), np.log(y)))
SYS = []   # every static system of rows c and d: dict(kind, name, Mb (Baryons, SI), rfar, radii [m], meta)
for c in XC:
    nm = c["name"]
    with fits.open(os.path.join(XD, nm, f"{nm}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    with fits.open(os.path.join(XD, nm, f"{nm}_mstar.fits")) as h: st = h[2].data.copy()
    gr = np.array(gas["RADIUS"], float) * rg500; gM = np.array(gas["MGAS"], float); sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float)
    rfar = 3 * c["R200_kpc"]; rsys = c["R200_kpc"]; rg = np.geomspace(0.5, rsys, 1500)          # A2: baryons truncated at R_sys = R200
    B = L.Baryons(rg * KPC, np.array([(ll(gr, gM, t, rsys) + ll(sr, sM, min(t, sr[-1]), rsys)) * MS for t in rg]), G)
    SYS.append(dict(kind="xcop", name=nm, Mb=B, rfar=rfar * KPC, radii=np.array([z["r_kpc"] for z in c["rows"]]) * KPC, c=c, r500=c["r500"] * KPC))
q5src = open(os.path.join(CL6, "QX5_cluster_terms", "qx5.py")).read()
Q5 = dict(os=os, np=np, math=math, DATA=os.path.join(REPO, "real_research", "data"))
exec(compile(q5src[q5src.index("def groups():"):q5src.index("XC, SP, EL, LE, GR = ")], "qx5.py:groups", "exec"), Q5)
GR = Q5["groups"]()
for gp in GR:
    sg = math.log(gp["g5"] / (gp["pts"][0]["M_gas"])) / math.log(gp["R5"] / gp["R25"]); rfar = 4.5 * gp["R5"]; rin = 0.1 * gp["R25"]; rsys = 1.5 * gp["R5"]   # A2
    for s in (0.0, 1.0):
        def Mbk(t, gp=gp, sg=sg, s=s, rin=rin, rfar=rfar):
            g25 = gp["pts"][0]["M_gas"]
            if t <= rin: return (1 + s) * g25 * (rin / gp["R25"]) ** sg * (t / rin) ** 3
            return (1 + s) * g25 * (min(t, rsys) / gp["R25"]) ** sg
        rg = np.geomspace(0.5, rsys, 1200)
        B = L.Baryons(rg * KPC, np.array([Mbk(t) * MS for t in rg]), G)
        SYS.append(dict(kind="group", name=gp["name"], s=s, Mb=B, rfar=rfar * KPC, radii=np.array([gp["R25"], gp["R5"]]) * KPC, gp=gp))
P(f"\nsystems: {sum(1 for s in SYS if s['kind'] == 'xcop')} X-COP clusters, {sum(1 for s in SYS if s['kind'] == 'group')} group brackets")

def run_arm(tag, f, X=XCL, self_grav=True, cap=True, kinds=("xcop", "group")):
    """continuation over the frozen c_s grid for every system; per (system, c_s): M_L at the gate radii, M_d at R500 (or R5), r_c, max mu_eff r."""
    fn = os.path.join(PARTS, f"{tag}_{f}.json")
    if os.path.exists(fn): return json.load(open(fn))
    a0 = L.A0[f]; rho = RHO[f]; out = {}
    for S in SYS:
        if S["kind"] not in kinds: continue
        key = S["name"] + ("" if S["kind"] == "xcop" else f"|s{int(S['s'])}")
        r1 = 100 * MPC if cap else S["rfar"]
        grid = L.Grid(S["Mb"], 1.0 * KPC, r1, h=0.01)
        st0 = L.shoot_fast(grid, 0, 0, 1, 0, X, G, a0, -3e12 if S["kind"] == "xcop" else -1e12, self_grav=self_grav, cap=cap, first=True)
        rec = dict(nodust=None, cs=[], ok=[], ML=[], Md500=[], rc=[], mur=[], Phi0=[])
        if not st0["ok"]:
            rec["nodust"] = dict(ok=False, reason=st0["reason"]); out[key] = rec; continue
        MLn, _, _ = L.eval_fast(st0, S["radii"], grid, G, a0); rec["nodust"] = dict(ok=True, ML=(MLn / MS).tolist(), rc=st0["rc"], Phi0=st0["Phi0"])
        Pv = st0["Phi0"]; alive = True
        for cs in CS:
            if not alive:
                rec["cs"].append(float(cs)); rec["ok"].append(False); rec["ML"].append(None); rec["Md500"].append(None); rec["rc"].append(None); rec["mur"].append(None); rec["Phi0"].append(None); continue
            cs2 = (cs * 1e3) ** 2
            st = L.shoot_fast(grid, 1, 4 * math.pi * rho, cs2, 0, X, G, a0, Pv, self_grav=self_grav, cap=cap)
            if not st["ok"]:
                alive = False; rec["cs"].append(float(cs)); rec["ok"].append(False); rec["ML"].append(None); rec["Md500"].append(None); rec["rc"].append(None); rec["mur"].append(None); rec["Phi0"].append(None); continue
            Pv = st["Phi0"]; ML, Md, Ph = L.eval_fast(st, S["radii"], grid, G, a0)
            rr = np.exp(st["u"]); rho_tot = rho * np.exp(np.minimum(-st["Phi"] / cs2, 700.0)); mur = float(np.max(np.sqrt(4 * math.pi * G * rho_tot) / (cs * 1e3) * rr))
            Mr = L.eval_fast(st, np.array([S["radii"][-1]]), grid, G, a0)[1][0]
            rec["cs"].append(float(cs)); rec["ok"].append(True); rec["ML"].append((ML / MS).tolist()); rec["Md500"].append(float(Mr / S["Mb"](S["radii"][-1])))
            rec["rc"].append(float(st["rc"] / KPC) if st["rc"] else None); rec["mur"].append(mur); rec["Phi0"].append(float(Pv))
        out[key] = rec
    json.dump(out, open(fn, "w")); return out

def grade_xcop(arm, f):
    """G-X per c_s from an arm's records."""
    a0 = A0Q[f]; res = []
    names = [c["name"] for c in XC]
    for j, cs in enumerate(CS):
        if not all(arm[n]["ok"][j] for n in names):
            bad = [n for n in names if not arm[n]["ok"][j]]; res.append(dict(cs=float(cs), PASS=False, reason=f"no static capped state for {bad}")); continue
        lut = {n: arm[n]["ML"][j] for n in names}
        def model(c, z, a0_):
            i = [round(zz["x"], 3) for zz in c["rows"]].index(round(z["x"], 3)); return lut[c["name"]][i]
        g = gateQ2(model)[f]
        res.append(dict(cs=float(cs), PASS=bool(g["PASS"]), mean=g["mean"], rms=g["rms"], Md500_med=float(np.median([arm[n]["Md500"][j] for n in names])),
                        mur_max=float(max(arm[n]["mur"][j] for n in names))))
    return res

def grade_groups(arm, f):
    res = []
    for j, cs in enumerate(CS):
        keys = [k for k in arm if "|s" in k]
        if not all(arm[k]["ok"][j] for k in keys):
            res.append(dict(cs=float(cs), PASS=False, reason=f"no static capped state for {sum(1 for k in keys if not arm[k]['ok'][j])} group brackets")); continue
        gm = {}; ch = []
        for s in (0, 1):
            d = []
            for gp in GR:
                ML = arm[f"{gp['name']}|s{s}"]["ML"][j]
                for p, m in zip(gp["pts"], ML):
                    d.append(math.log10(p["M_obs"] / m))
                Mb5 = (1 + s) * gp["g5"]; ch.append((ML[1] - Mb5) / (XCL * Mb5))
            gm[s] = float(np.mean(d))
        lo_, hi_ = sorted([gm[0], gm[1]])
        res.append(dict(cs=float(cs), PASS=bool(lo_ <= 0.05 and hi_ >= -0.05), mean_star0=gm[0], mean_star1=gm[1], charge_over_share_med=float(np.median(ch)),
                        mur_max=float(max(arm[k]["mur"][j] for k in keys))))
    return res

def interval(res):
    ps = [r["cs"] for r in res if r["PASS"]]
    if not ps: return None, []
    srt = sorted(ps); runs = []; grid = sorted(float(c) for c in CS); idx = [grid.index(p) for p in srt]; s0 = idx[0]; pv = idx[0]
    for i in idx[1:]:
        if i != pv + 1: runs.append((grid[s0], grid[pv])); s0 = i
        pv = i
    runs.append((grid[s0], grid[pv])); return [srt[0], srt[-1]], runs

# ---------------- KA4: no dust reproduces the record
P("\nROWS c, d graded (self-consistent isothermal dust, self-gravity, share cap 5.41)")
ARMS = {}
for f in L.FOOT:
    ARMS[("graded", f)] = run_arm("graded", f)
    arm = ARMS[("graded", f)]
    lut = {c["name"]: arm[c["name"]]["nodust"]["ML"] for c in XC}
    def model(c, z, a0_, lut=lut):
        i = [round(zz["x"], 3) for zz in c["rows"]].index(round(z["x"], 3)); return lut[c["name"]][i]
    g = gateQ2(model)[f]; ref = {"canonical": 0.4675, "alt": 0.4345}[f]
    RES["KA"][f"KA4 X-COP no dust {f}"] = dict(value=g["mean"], ref=ref, ok=bool(abs(g["mean"] - ref) <= 2e-3))
    gm = {}
    for s in (0, 1):
        d = [math.log10(p["M_obs"] / m) for gp in GR for p, m in zip(gp["pts"], arm[f"{gp['name']}|s{s}"]["nodust"]["ML"])]; gm[s] = float(np.mean(d))
    refg = {"canonical": (0.196, 0.359), "alt": (0.158, 0.320)}[f]
    gl = {}                                                     # A3 (post hoc): the machinery's check is the no-dust law with the cap off
    for s in (0, 1):
        dl = []
        for gp in GR:
            for p in gp["pts"]:
                rm_ = p["r_kpc"] * KPC; Mb_ = p["M_gas"] * (1 + s); Ml_ = L.law_g(G * Mb_ * MS / rm_ ** 2, L.A0[f]) * rm_ ** 2 / G / MS; dl.append(math.log10(p["M_obs"] / Ml_))
        gl[s] = float(np.mean(dl))
    dv = max(abs(gl[1] - refg[0]), abs(gl[0] - refg[1])); dv_frozen = max(abs(gm[1] - refg[0]), abs(gm[0] - refg[1]))
    RES["KA"][f"KA4 groups no dust {f}"] = dict(value_cap_off=[gl[1], gl[0]], ref=refg, ok=bool(dv <= 2e-3), A3="post hoc: checked with the cap off",
                                                 capped_no_dust_reported=[gm[1], gm[0]], frozen_reading_ok=bool(dv_frozen <= 2e-3))
    P(f"KA4 [{f}] no dust: X-COP mean {g['mean']:+.4f} (QX2 {ref:+.4f}); groups, cap off (A3) [{gl[1]:+.4f}, {gl[0]:+.4f}], capped (reported) [{gm[1]:+.4f}, {gm[0]:+.4f}] (QX5 {refg}; frozen reading {'PASS' if dv_frozen <= 2e-3 else 'FAIL'}) -> "
      f"{'PASS' if RES['KA'][f'KA4 X-COP no dust {f}']['ok'] and RES['KA'][f'KA4 groups no dust {f}']['ok'] else 'FAIL'}  [{time.time() - T0:.0f} s]")
    rx = grade_xcop(arm, f); rg_ = grade_groups(arm, f); ivx, runsx = interval(rx); ivg, runsg = interval(rg_)
    okx = [r for r in rx if "rms" in r]; best = min(okx, key=lambda r: r["rms"]) if okx else None
    RES["rows"][f"c {f}"] = dict(interval=ivx, runs=runsx, points=rx, closest=best)
    RES["rows"][f"d {f}"] = dict(interval=ivg, runs=runsg, points=rg_)
    fold = next((r["cs"] for r in rx if "reason" in r), None)
    P(f"  [{f}] row c X-COP: interval {ivx}; closest rms {best['rms']:.3f} (mean {best['mean']:+.3f}) at c_s {best['cs']:.0f} km/s; first c_s with no static state: {fold}" if best else f"  [{f}] row c: no state")
    for r in rx[::8]:
        if "rms" in r: P(f"     c_s {r['cs']:7.1f}: mean {r['mean']:+.3f} rms {r['rms']:.3f} dust/baryons at R500 (median) {r['Md500_med']:.3g}  max mu r {r['mur_max']:.2f}")
        else: P(f"     c_s {r['cs']:7.1f}: {r['reason']}")
    P(f"  [{f}] row d groups: interval {ivg} runs {runsg}")
    for r in rg_[::8]:
        if "mean_star0" in r: P(f"     c_s {r['cs']:7.1f}: bracket [{r['mean_star1']:+.3f}, {r['mean_star0']:+.3f}] charge/share {r['charge_over_share_med']:.2f} max mu r {r['mur_max']:.2f} -> {'P' if r['PASS'] else 'F'}")
        else: P(f"     c_s {r['cs']:7.1f}: {r['reason']}")

# ---------------- MK1's reading (QX2's HSE potential, zero 3 R200, no self-gravity, no cap): KA1 with the quadratic, exponential reported
P("\nMK1's reading (HSE potential) - KA1 with the quadratic; the exponential reported")
for c in XC:
    rr, psi = Q2["psi_profile"](c); c["_psi"] = (rr, psi)
def MK_read(c, r_kpc, kind, par, f):
    rr, psi = c["_psi"]; m = rr <= r_kpc
    if kind == "quad": dens = par * np.abs(psi) / (4 * math.pi * G)
    else: dens = RHO[f] * np.expm1(np.minimum(np.abs(psi) / par, 700.0))
    x = rr[m] * KPC; return min(float(np.trapz(4 * math.pi * x ** 2 * dens[m], x)) / MS, 1e30)     # 1e30 Msun: overflow guard (that c_s fails by far)
def gate_read(kind, par):
    out = {}
    for f in L.FOOT:
        def model(c, z, a0_, f=f):
            Mt = z["M_b"] + MK_read(c, z["r_kpc"], kind, par, f); return Q2["law_M"](Mt, z["r_kpc"], a0_)[0]
        out[f] = gateQ2(model)[f]
    return out
MU = 10 ** np.arange(-1.0, 1.5001, 0.01)
sc = [gate_read("quad", (m / MPC) ** 2) for m in MU]
for f, (rm, mm) in (("canonical", (0.263, 1.35)), ("alt", (0.255, 1.26))):
    rms = np.array([s[f]["rms"] for s in sc]); i = int(np.argmin(rms)); ps = any(s[f]["PASS"] for s in sc)
    ok = (not ps) and abs(rms[i] - rm) <= 2e-3 and abs(MU[i] / mm - 1) <= 0.03
    RES["KA"][f"KA1 row c MK1 reading {f}"] = dict(min_rms=float(rms[i]), mu=float(MU[i]), ref=(rm, mm), ok=bool(ok))
    P(f"KA1 [{f}] quadratic, MK1's X-COP reading: empty {not ps}; min rms {rms[i]:.3f} at mu {MU[i]:.3g} (MK1 {rm} at {mm}) -> {'PASS' if ok else 'FAIL'}")
for f in L.FOOT:
    rr_ = [gate_read("exp", (cs * 1e3) ** 2)[f] for cs in CS[::4]]
    i = int(np.argmin([r["rms"] for r in rr_])); RES["rows"][f"c MK1-reading exp {f}"] = dict(min_rms=rr_[i]["rms"], cs=float(CS[::4][i]), mean=rr_[i]["mean"], any_pass=bool(any(r["PASS"] for r in rr_)))
    P(f"  [{f}] exponential in MK1's reading (no self-gravity, no cap, HSE potential): any pass {RES['rows'][f'c MK1-reading exp {f}']['any_pass']}; min rms {rr_[i]['rms']:.3f} at c_s {CS[::4][i]:.0f}")
# groups MK1 reading with the quadratic
for gp in GR:
    sl = math.log(gp["M5"] / gp["M25"]) / math.log(gp["R5"] / gp["R25"]); rz = 3 * 1.5 * gp["R5"]
    rr = np.geomspace(1e-3 * gp["R25"], rz, 4000); Mr = gp["M25"] * (rr / gp["R25"]) ** sl
    gacc = G * Mr * MS / (rr * KPC) ** 2; seg = 0.5 * (gacc[1:] + gacc[:-1]) * np.diff(rr * KPC)
    gp["_psi"] = (rr, -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]))
def gate_g_read(mu2):
    out = {}
    for f, a0 in A0Q.items():
        gm = {}
        for s in (0.0, 1.0):
            d = []
            for gp in GR:
                rr, psi = gp["_psi"]
                for p in gp["pts"]:
                    m = rr <= p["r_kpc"]; x = rr[m] * KPC; mk = float(np.trapz(4 * math.pi * x ** 2 * mu2 * np.abs(psi[m]) / (4 * math.pi * G), x)) / MS
                    Mt = p["M_gas"] * (1 + s) + mk; rm_ = p["r_kpc"] * KPC; Ml = L.law_g(G * Mt * MS / rm_ ** 2, a0) * rm_ ** 2 / G / MS
                    d.append(math.log10(p["M_obs"] / Ml))
            gm[s] = float(np.mean(d))
        lo_, hi_ = sorted(gm.values()); out[f] = lo_ <= 0.05 and hi_ >= -0.05
    return out
MU2 = 10 ** np.arange(-1.0, 1.0001, 0.01); sg_ = [gate_g_read((m / MPC) ** 2) for m in MU2]
for f, ref in (("canonical", (0.912, 1.514)), ("alt", (0.759, 1.380))):
    ps = [MU2[i] for i, s in enumerate(sg_) if s[f]]
    iv = (min(ps), max(ps)) if ps else None; ok = bool(iv and abs(math.log10(iv[0] / ref[0])) <= 0.0101 and abs(math.log10(iv[1] / ref[1])) <= 0.0101)
    RES["KA"][f"KA1 row d MK1 reading {f}"] = dict(interval=iv, ref=ref, ok=ok)
    P(f"KA1 [{f}] quadratic, MK1's groups reading: {None if not iv else (round(iv[0], 3), round(iv[1], 3))} (MK1 {ref}) -> {'PASS' if ok else 'FAIL'}")

# ============================================================== row g: Solar System (EW2's lines with the exponential dust)
P("\nROW g Solar System (EW2: dg(Saturn) <= 7.0e-15 m/s^2, Q2 <= 9.0e-27 s^-2; Phi0 (600 km/s)^2)")
GM_SUN = 1.32712440018e20; AU = 1.495978707e11; R_SAT = 9.5826 * AU; R_SUN = 6.957e8; SAT, HEES = 7.0e-15, 9.0e-27
def solar(cs, f, phi0=(600e3) ** 2):
    cs2 = (cs * 1e3) ** 2; rr = np.geomspace(R_SUN, R_SAT, 4000)
    rho_r = RHO[f] * np.exp(np.minimum((phi0 + GM_SUN / rr) / cs2, 700.0)); M = float(np.trapz(4 * math.pi * rr ** 2 * rho_r, rr))
    dg = G * M / R_SAT ** 2; rho_1au = RHO[f] * math.exp(min((phi0 + GM_SUN / AU) / cs2, 700.0)); q2 = 4 * math.pi / 3 * G * rho_1au
    return dg, q2
for f in L.FOOT:
    ps = [cs for cs in CS if all(v <= l for v, l in zip(solar(cs, f), (SAT, HEES)))]
    lo_g = min(ps) if ps else None; hi_g = max(ps) if ps else None
    contiguous = bool(ps) and all(cs in ps for cs in CS if cs >= lo_g)
    lo_cap = min([cs for cs in CS if all(v <= l for v, l in zip(solar(cs, f, phi0=(401e3 if f == 'canonical' else 415e3) ** 2), (SAT, HEES)))], default=None)
    RES["rows"][f"g {f}"] = dict(interval=[lo_g, None] if contiguous else None, cs_min=lo_g, reported_capped_MW_cs_min=lo_cap)
    P(f"  [{f}] passes for c_s >= {lo_g:.1f} km/s on the grid (contiguous above: {contiguous}); with MK1's capped Milky Way potential ((401 / 415 km/s)^2, reported) c_s >= {lo_cap:.1f}")
dq = 6223.346
mu = dq / MPC; dgq = mu ** 2 * (GM_SUN / 2 + (600e3) ** 2 * R_SAT / 3)
RES["KA"]["KA1 row g quadratic"] = dict(value=dgq, ok=bool(abs(dgq / SAT - 1) <= 1e-3))
P(f"  KA1 quadratic through the Saturn code at MK1's bound 6223.35: dg {dgq:.4e} (line 7.0e-15) -> {'PASS' if abs(dgq / SAT - 1) <= 1e-3 else 'FAIL'}")

# ============================================================== row h: SCS1 (clusters, groups from the arms; galaxies here)
P("\nROW h SCS1: max_r mu_eff(r) r <= 2 pi in every static state")
def gal_mur(f, lm, xa=0.2, cs_list=CS):
    a0 = L.A0[f]; M = 2.5 * 10 ** lm * MS; rM = math.sqrt(G * M / a0); s = math.sqrt(G * M * a0)
    alpha = 4 * math.pi * RHO[f] * rM ** 3 / M; Bh = L.hernquist(xa); grid = L.Grid(Bh, 1e-4, 1e5, h=0.01)
    st0 = L.shoot_fast(grid, 0, 0, 1, 0, XP[f], 1.0, 1.0, -10.0, first=True); Pv = st0["Phi0"]; out = []; alive = True
    for cs in cs_list:
        if not alive: out.append(None); continue
        beta_inv = (cs * 1e3) ** 2 / s
        st = L.shoot_fast(grid, 1, alpha, beta_inv, 0, XP[f], 1.0, 1.0, Pv)
        if not st["ok"]: alive = False; out.append(None); continue
        Pv = st["Phi0"]; xx = np.exp(st["u"]); rho_dimless = (alpha / (4 * math.pi)) * np.exp(np.minimum(-st["Phi"] / beta_inv, 700.0))
        # mu_eff^2 = 4 pi G rho / c_s^2; in units r_M: 4 pi rho_dimless (M_b/r_M^3) G / c_s^2 * r_M^2 = 4 pi rho_dimless * s / c_s^2 (a0 r_M = s)
        out.append(float(np.max(np.sqrt(4 * math.pi * rho_dimless / beta_inv) * xx)))
    return out
RH = {}
for f in L.FOOT:
    gal = {lm: gal_mur(f, lm) for lm in (9, 10, 11)}
    arm = ARMS[("graded", f)]; per = []
    for j, cs in enumerate(CS):
        vals = [gal[lm][j] for lm in gal] + [arm[k]["mur"][j] for k in arm]
        if any(v is None for v in vals): per.append(dict(cs=float(cs), PASS=False, reason="a static state is missing (fold)", max=None)); continue
        m = max(vals); per.append(dict(cs=float(cs), PASS=bool(m <= 2 * math.pi), max=m))
    iv, runs = interval(per); RH[f] = dict(interval=iv, runs=runs, points=per, galaxies={str(k): v for k, v in gal.items()})
    P(f"  [{f}] row h: interval {iv} runs {runs}; at 1000 / 500 / 300 / 200 / 100 km/s max mu r = " + " / ".join(
        f"{next((p['max'] for p in per if abs(p['cs'] - c_) / c_ < 0.03), None)}" for c_ in (1000, 500, 300, 200, 100)))
    for xa in (0.1, 0.4):
        alt = gal_mur(f, 11, xa=xa, cs_list=CS[:97]); RH[f][f"log M 11 x_a {xa} (reported)"] = alt
RES["rows"]["h"] = RH

# ============================================================== KA2, KA3
P("\nKA2 Emden"); e = L.emden_check()
okE = abs(e["contrast_6451"] / 14.04 - 1) <= 2e-3 and e["sis_ratio_min"] >= 0.97 and e["sis_ratio_max"] <= 1.03
RES["KA"]["KA2 Emden"] = dict(**e, ok=bool(okE)); P(f"  contrast at xi 6.451: {e['contrast_6451']:.4f} (14.04); e^-psi xi^2/2 on 3e3-1e4: [{e['sis_ratio_min']:.4f}, {e['sis_ratio_max']:.4f}] -> {'PASS' if okE else 'FAIL'}")
f = "canonical"; a0 = L.A0[f]; M = 2.5 * 10 ** 10.5 * MS; rM = math.sqrt(G * M / a0); s = math.sqrt(G * M * a0); alpha = 4 * math.pi * RHO[f] * rM ** 3 / M
Bh = L.hernquist(0.2); gridh = L.Grid(Bh, 1e-5, 1e5, h=0.01); st0 = L.shoot_fast(gridh, 0, 0, 1, 0, XP[f], 1.0, 1.0, -10.0, first=True); Pv = st0["Phi0"]
for cs in CS[CS >= 150 * 0.999]:                                   # the branch from no dust down to 150 km/s (A1)
    stf = L.shoot_fast(gridh, 1, alpha, (cs * 1e3) ** 2 / s, 0, XP[f], 1.0, 1.0, Pv); Pv = stf["Phi0"] if stf["ok"] else Pv
d = L.Dust("exp", rho_bar=alpha / (4 * math.pi), cs2=(CS[CS >= 150 * 0.999][-1] * 1e3) ** 2 / s, Gc=1.0)
stx = L.solve_capped(Bh, d, XP[f], 1.0, 1.0, 1e-5, 1e5, 1e6, stf["Phi0"], n_scan=41, span=(0.995, 1.01))
uu = np.linspace(math.log(1e-5), math.log(stx["rc"]), 200001); yy = stx["sol"].sol(uu); xx = np.exp(uu)
direct = float(np.trapz(4 * math.pi * xx ** 3 * d(yy[0]), uu)); rel3 = abs(direct / stx["Md_c"] - 1); relf = abs(stf["Md_c"] / stx["Md_c"] - 1)
RES["KA"]["KA3 static dust direct integral"] = dict(rel=rel3, fast_vs_dop853_Md=relf, Md_over_Mb=stx["Md_c"], ok=bool(rel3 <= 1e-5 and stx["Md_c"] > 0))
P(f"KA3 point mass (log M_b 10.9 incl. k, c_s {CS[CS >= 150 * 0.999][-1]:.1f}, on the branch): dust mass from the ODE {stx['Md_c']:.6g} M_b vs direct quadrature {direct:.6g} (rel {rel3:.1e}); "
  f"fast RK4 path rel {relf:.1e} -> {'PASS' if rel3 <= 1e-5 and stx['Md_c'] > 0 else 'FAIL'}")

ka_ok = all(v["ok"] for v in RES["KA"].values()); RES["KA_all_pass"] = ka_ok
P(f"\nKnown answers here: {sum(v['ok'] for v in RES['KA'].values())} of {len(RES['KA'])} PASS -> {'ALL PASS' if ka_ok else 'A KNOWN ANSWER FAILED'}  [{time.time() - T0:.0f} s]")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "mk2_rows.json"), "w"), indent=1)
open(os.path.join(HERE, "mk2_rows.out"), "w").write("\n".join(OUT + [L.NOTE]) + "\n")

# ============================================================== MUTATE arms on rows c, d
MU_ = dict(lane="MK2", file="mk2_rows_MUTATE", arms={})
for tag, kw in (("M-NOCAP", dict(cap=False)), ("M-NOSELF", dict(self_grav=False)), ("M-2X", dict(X=2 * XCL))):
    for f in L.FOOT:
        arm = run_arm(tag, f, **kw); rx = grade_xcop(arm, f); rg_ = grade_groups(arm, f); ivx, rx_runs = interval(rx); ivg, rg_runs = interval(rg_)
        okx = [r for r in rx if "rms" in r]; best = min(okx, key=lambda r: r["rms"]) if okx else None
        MU_["arms"][f"{tag} {f}"] = dict(c_interval=ivx, c_closest=best, d_interval=ivg, d_runs=rg_runs,
                                          primary_c=RES["rows"][f"c {f}"]["interval"], primary_c_closest=RES["rows"][f"c {f}"]["closest"], primary_d=RES["rows"][f"d {f}"]["interval"])
        PM(f"{tag} [{f}]: row c {ivx} (closest rms {best['rms'] if best else None}) vs primary {RES['rows'][f'c {f}']['interval']} (closest {RES['rows'][f'c {f}']['closest']['rms'] if RES['rows'][f'c {f}']['closest'] else None}); "
           f"row d {ivg} vs primary {RES['rows'][f'd {f}']['interval']}  [{time.time() - T0:.0f} s]")
json.dump(clean(MU_), open(os.path.join(HERE, "mk2_rows_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "mk2_rows_MUTATE.out"), "w").write("\n".join(OUTM + [L.NOTE]) + "\n")
P(f"done [{time.time() - T0:.0f} s]")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
