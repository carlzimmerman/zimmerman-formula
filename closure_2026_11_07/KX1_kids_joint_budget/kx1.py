#!/usr/bin/env python3
"""KX1 (FROZEN_CRITERIA.md db8ffafa83): QX10's KiDS kill of the late-heated window, re-graded at 100-300 kpc with a joint
systematic budget (kSZ hot gas, two-halo, isolation, stellar-mass shift, ESD calibration). Both footings, never pooled.
  python3 kx1.py            -> kx1.json / kx1.out   (KA1-KA3, main grade, M2 law control, reported readings)
  python3 kx1.py --mutate   -> kx1_MUTATE.json / .out (M1: the window at 4x sector mass)
kappa = 1/2 FITTED; not theory closed. Adopts nothing. One thread, no download."""
import os, sys, json, math, io, contextlib, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "kx1_MUTATE" if MUT else "kx1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# ---------------------------------------------------------------- QX10 iter_2, executed read-only (its __main__ is not run)
Q10D = os.path.join(REPO, "closure_2026_11_06", "QX10_window_hardening", "iter_2_capture_dynamics")
Q10 = os.path.join(Q10D, "qx10_i2.py")
argv0, sys.argv = sys.argv, [Q10]
NS = {"__file__": Q10, "__name__": "qx10_reused"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(Q10).read(), Q10, "exec"), NS)
sys.argv = argv0
Q10J = json.load(open(os.path.join(Q10D, "qx10_i2.json")))
solve_static, Mdust_at, pointmass, K_of, r_ta = (NS[k] for k in ("solve_static", "Mdust_at", "pointmass", "K_of", "r_ta"))
grade_cell, baselines, glaw_SI = NS["grade_cell"], NS["baselines"], NS["glaw_SI"]
FCAP, RR, A0K, ACC, CELLS = NS["FCAP"], NS["R"], NS["A0K"], NS["ACC"], NS["CELLS"]
Q5NS = None
G_SI, MS, KPC_M = NS["G_SI"], NS["MS"], NS["KPC_M"]
PC_M = KPC_M / 1e3; GPC = 4.52e-30          # QX5's lensing constants
FOOTS = ("canonical", "alt")

# ---------------------------------------------------------------- B21 Fig-9 isolated lenses, four mass bins, full covariance
BD = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
LMID = [9.4, 10.45, 10.7, 10.9]; LMIN = [8.5, 10.3, 10.6, 10.8]
CONV = 4 * GPC * PC_M
BIN = []
for i, lm in enumerate(LMID, 1):
    a = np.loadtxt(os.path.join(BD, f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt"), comments="#")
    BIN.append(dict(lm=lm, gbar=a[:, 0], y=CONV * a[:, 1] / a[:, 4], err=CONV * a[:, 3] / a[:, 4], bias=a[:, 4]))
cv = np.loadtxt(os.path.join(BD, "Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt"), comments="#")
for b, B in enumerate(BIN):
    n = len(B["gbar"]); C = np.zeros((n, n))
    for row in cv:
        if abs(row[0] - LMIN[b]) < 1e-6 and abs(row[1] - LMIN[b]) < 1e-6:
            i = int(np.argmin(np.abs(B["gbar"] - row[2]) / B["gbar"])); j = int(np.argmin(np.abs(B["gbar"] - row[3]) / B["gbar"]))
            C[i, j] = row[4] / row[6]
    B["C"] = CONV ** 2 * C
    B["r"] = np.sqrt(G_SI * 10 ** B["lm"] * MS / B["gbar"]) / KPC_M          # QX10's conversion, kpc
    B["win"] = (B["r"] >= 100.0) & (B["r"] <= 300.0)

# ---------------------------------------------------------------- CW6 hot-gas table (cw6_gas.out)
CW6 = os.path.join(REPO, "cw_lanes_2026_11_04", "CW6_lensing_measured_gas", "cw6_gas.out")
RG = np.array([50, 100, 200, 300, 500, 1000, 2000], float)
GAS = {}
for ln in open(CW6):
    t = ln.split()
    if len(t) >= 10 and t[1] == "lm" and (t[0] == "FIXED" or (t[0][0] in "PB" and t[0][1:].isdigit())):
        GAS.setdefault(t[0], {})[float(t[2])] = np.array([float(x) for x in t[3:10]])
PROFS = [k for k in GAS if k != "FIXED"]          # P1-P6, B1-B5
GLM = sorted(GAS["P1"])
def hot_ratio(prof, lm, r):
    """M_hot(<r)/M*: linear in log M* and log r on CW6's grid; below 10.0 the 10.0 row (frozen); r clipped to the grid."""
    tab = GAS[prof]; lmc = min(max(lm, GLM[0]), GLM[-1])
    k = int(np.searchsorted(GLM, lmc)); k = min(max(k, 1), len(GLM) - 1)
    l0, l1 = GLM[k - 1], GLM[k]; w = (lmc - l0) / (l1 - l0)
    row = (1 - w) * tab[l0] + w * tab[l1]
    lr = np.log(np.clip(r, RG[0], RG[-1]))
    return np.interp(lr, np.log(RG), row)

# ---------------------------------------------------------------- two-halo template (CFG4_switch / FP1 E), CFG15 caps
CFGD = os.path.join(REPO, "campaign_fresh_gravity"); sys.path.insert(0, CFGD)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG7_common as C7
    C4 = C7.C4
    SWJ = json.load(open(os.path.join(CFGD, "CFG4_switch_results.json")))["numbers"]
    ns = {"np": np, "math": math, "os": os, "C": C4, "A0": C4.A0, "time": time, "t3": time.time(), "P": lambda *a, **k: None,
          "DTA": {0.25: (SWJ["D1"]["0.25"]["one_plus_delta_ta"], SWJ["D1"]["0.25"]["delta_lin_ta"])}}
    GK4 = C4.exec_slices(os.path.join(CFGD, "CFG4_switch.py"), [('GK = {"np": np', 'check("K3 CONTROL')], ns=ns, name="cfg4_switch_slices")[0]["GK"]
sys.path.remove(CFGD)
RD = [np.asarray(GK4["Rd"][b], float) for b in range(4)]; T2H = [np.asarray(GK4["T2H"][b], float) for b in range(4)]
BCAP = {"canonical": [1.11, 1.35, 1.44, 1.57], "alt": [1.14, 1.39, 1.49, 1.63]}     # CFG15 D1, collapse threshold
def g2h(b, r_kpc):    # g_obs contribution per unit bias, at R = r
    return CONV * np.interp(np.log(r_kpc / 1e3), np.log(RD[b]), T2H[b])

# ---------------------------------------------------------------- budget constants (frozen)
SIG_A20 = 0.18749889327551758          # CFG96 sigma_A20 (results json)
SPLIT = 0.18                           # CFG116 early-late amplitude, dex
SIG_ISO = math.log10(1 + SIG_A20 * (1 - 10 ** -SPLIT))
DELTA_M = 0.1884                       # GH9 median, CW6 B3


# ---------------------------------------------------------------- sector profiles
SEC = {}
def sector(cell, foot, lm, mult=1.0):
    key = (cell, foot, round(lm, 6), mult)
    if key not in SEC:
        if cell is None or mult == 0.0: SEC[key] = None
        else:
            Mb = 10 ** lm; lam = CELLS[cell][0] * 1e3
            SEC[key] = solve_static(pointmass(Mb), mult * FCAP * RR * Mb, K_of(lam), r_ta(Mb), A0K[foot])
    return SEC[key]


def model(B, sel, foot, cell, mult, prof, dM):
    """g_obs model at the selected points: glaw(g_bar + g_hot + g_sector), masses scaled by 10^dM (r is invariant)."""
    s = 10 ** dM; lm = B["lm"] + dM; r = B["r"][sel]; Mb = 10 ** lm
    gN = B["gbar"][sel] * s
    if prof is not None: gN = gN + G_SI * hot_ratio(prof, lm, r) * Mb * MS / (r * KPC_M) ** 2
    sol = sector(cell, foot, lm, mult)
    if sol is not None: gN = gN + G_SI * np.array([Mdust_at(sol, x) for x in r]) * MS / (r * KPC_M) ** 2
    return glaw_SI(gN, A0K[foot] * ACC)


def loga(B, sel, m, bfac, foot, b):
    y = B["y"][sel] - bfac * g2h(b, B["r"][sel]); Ci = np.linalg.inv(B["C"][np.ix_(sel, sel)])
    F = m @ Ci @ m; a = (m @ Ci @ y) / F; sa = F ** -0.5
    return math.log10(a) if a > 0 else float("nan"), sa / (abs(a) * math.log(10)), a


def budget(B, b, sel, foot, cell, mult):
    """central log10 a and each budget term for one model (cell None = the law)."""
    bc = BCAP[foot][b]; cen_b = bc / 2; sb = bc / math.sqrt(12)
    m0 = model(B, sel, foot, cell, mult, "P1", 0.0)
    la, sstat, a = loga(B, sel, m0, cen_b, foot, b)
    gas = [loga(B, sel, model(B, sel, foot, cell, mult, p, 0.0), cen_b, foot, b)[0] for p in PROFS]
    s_gas = (max(gas) - min(gas)) / 2
    s_2h = abs(loga(B, sel, m0, cen_b + sb, foot, b)[0] - loga(B, sel, m0, cen_b - sb, foot, b)[0]) / 2
    lp = loga(B, sel, model(B, sel, foot, cell, mult, "P1", +DELTA_M), cen_b, foot, b)[0]
    lmn = loga(B, sel, model(B, sel, foot, cell, mult, "P1", -DELTA_M), cen_b, foot, b)[0]
    s_M = abs(lp - lmn) / 2
    s_cal = math.log10(1 + float(np.max(np.abs(1 - B["bias"][sel]))))
    terms = dict(stat=sstat, gas=s_gas, two_halo=s_2h, iso=SIG_ISO, mstar=s_M, cal=s_cal)
    tot = math.sqrt(sum(v ** 2 for v in terms.values()))
    # no-correction reading (P1 gas off, no 2h): reported
    raw = loga(B, sel, model(B, sel, foot, cell, mult, None, 0.0), 0.0, foot, b)[0]
    return dict(loga=la, a=a, terms=terms, sigma_tot=tot, gas_by_profile=dict(zip(PROFS, gas)), loga_raw=raw, m=m0)


def label(rows):
    npow = sum(1 for x in rows if x["W"] >= 2 * x["sig_win"])
    nkill = sum(1 for x in rows if x["z"] > 2)
    if len(rows) - npow >= 3: return "NO POWER", npow, nkill
    return ("KILL HOLDS" if nkill >= 2 else "KILL SOFTENS"), npow, nkill


def grade(foot, cell, mult, selname="win"):
    rows = []
    for b, B in enumerate(BIN):
        sel = B["win"] if selname == "win" else np.ones(len(B["y"]), bool)
        L = budget(B, b, sel, foot, None, 0.0); Wd = budget(B, b, sel, foot, cell, mult)
        E = L["loga"]; W = L["loga"] - Wd["loga"]
        rows.append(dict(bin=b + 1, lm=B["lm"], n=int(sel.sum()), r_kpc=[float(x) for x in B["r"][sel]],
                         E=E, sig_law=L["sigma_tot"], W=W, sig_win=Wd["sigma_tot"], line=E + 2 * Wd["sigma_tot"],
                         z=(W - E) / Wd["sigma_tot"], z_law=-E / L["sigma_tot"], terms_law=L["terms"], terms_win=Wd["terms"],
                         E_raw=L["loga_raw"], W_raw=L["loga_raw"] - Wd["loga_raw"], gas_law=L["gas_by_profile"]))
    lab, npow, nkill = label(rows)
    return dict(rows=rows, label=lab, n_power=npow, n_kill=nkill)


# ---------------------------------------------------------------- projected reading (reported)
RGRID = np.geomspace(1.0, 1.0e4, 2000)   # kpc
def esd_model(B, foot, cell, mult, Rk):
    lm = B["lm"]; Mb = 10 ** lm; r = RGRID
    M = Mb + hot_ratio("P1", lm, r) * Mb
    sol = sector(cell, foot, lm, mult)
    if sol is not None: M = M + np.array([Mdust_at(sol, x) for x in r])
    g = glaw_SI(G_SI * M * MS / (r * KPC_M) ** 2, A0K[foot] * ACC)
    Me = g * (r * KPC_M) ** 2 / G_SI / MS                 # Msun
    dM = np.diff(np.concatenate([[0.0], Me])); rm = r
    out = []
    for R in Rk:
        o = rm > R
        mcyl = Me[~o][-1] if (~o).any() else 0.0
        mcyl += float(np.sum(dM[o] * (1 - np.sqrt(1 - (R / rm[o]) ** 2))))
        # Sigma(R) = sum over shells of dM / (2 pi r sqrt(r^2 - R^2)) * (shell thickness factor) -> use z-integral of rho
        rho = np.gradient(Me, r) / (4 * math.pi * r ** 2)
        z = np.geomspace(1e-3, 1e4, 3000); rr = np.sqrt(R ** 2 + z ** 2)
        sig = 2 * np.trapz(np.interp(rr, r, rho, right=0.0), z)
        out.append(mcyl / (math.pi * R ** 2) - sig)       # Msun / kpc^2
    return CONV * np.array(out) / 1e6                        # per pc^2 -> g_obs


def projected(foot, cell, mult):
    rows = []
    for b, B in enumerate(BIN):
        sel = B["win"]; bc = BCAP[foot][b]
        mL = esd_model(B, foot, None, 0.0, B["r"][sel]); mW = esd_model(B, foot, cell, mult, B["r"][sel])
        lL = loga(B, sel, mL, bc / 2, foot, b)[0]; lW = loga(B, sel, mW, bc / 2, foot, b)[0]
        rows.append(dict(bin=b + 1, E=lL, W=lL - lW))
    return rows


# ================================================================ run
P(f"KX1 {'MUTATE (M1: window at 4x sector mass)' if MUT else 'main'}: QX10's KiDS kill re-graded at 100-300 kpc with a joint budget.")
P("kappa = 1/2 FITTED; not theory closed. Criteria db8ffafa83. Footings never pooled.")
P(f"points per bin in 100-300 kpc: {[int(B['win'].sum()) for B in BIN]}; sigma_iso {SIG_ISO:.4f} dex; delta_M {DELTA_M}")
RES = dict(lane="KX1", criteria="db8ffafa83", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed",
           sigma_iso=SIG_ISO, delta_M=DELTA_M, n_window=[int(B["win"].sum()) for B in BIN])

if not MUT:
    # KA1: QX10's G6 shifts and baselines, through its own grade_cell
    ka1 = []; mx = 0.0
    for f in FOOTS:
        bl = baselines(A0K[f]); d0 = abs(bl[0] - Q10J["baselines"][f][0]); mx = max(mx, d0)
        for c, (l0, pp) in CELLS.items():
            with contextlib.redirect_stdout(io.StringIO()):
                o = grade_cell(l0 * 1e3, A0K[f])
            sh = o["G6_mean"] - bl[0]; ref = Q10J["cells"][c][f]["G6_shift"]; mx = max(mx, abs(sh - ref))
            ka1.append(dict(cell=c, foot=f, shift=sh, qx10=ref, d=abs(sh - ref)))
    RES["KA1"] = dict(rows=ka1, max_d=mx, pass_=bool(mx == 0.0))
    P(f"KA1 QX10 G6 shifts + baselines via grade_cell: max |d| {mx:.1e} -> {'PASS' if mx == 0.0 else 'FAIL'}  "
      + ", ".join(f"{x['cell']}/{x['foot'][:3]} {x['shift']:+.3f}" for x in ka1))
    # KA2: gas interpolator at nodes
    d2 = max(abs(hot_ratio(p, lm, RG)[k] - GAS[p][lm][k]) for p in GAS for lm in GLM for k in range(len(RG)))
    RES["KA2"] = dict(max_d=float(d2), pass_=bool(d2 <= 1e-12))
    P(f"KA2 CW6 gas interpolator at grid nodes: max |d| {d2:.1e} -> {'PASS' if d2 <= 1e-12 else 'FAIL'}")
    # KA3: sector 0 gives W = 0
    d3 = max(abs(x["W"]) for f in FOOTS for x in grade(f, "C1", 0.0)["rows"])
    RES["KA3"] = dict(max_W=float(d3), pass_=bool(d3 == 0.0))
    P(f"KA3 sector mass 0: max |W_b| {d3:.1e} -> {'PASS' if d3 == 0.0 else 'FAIL'}")

RES["grade"] = {}
mult = 4.0 if MUT else 1.0
for f in FOOTS:
    RES["grade"][f] = {}
    for c in CELLS:
        g = grade(f, c, mult); RES["grade"][f][c] = g
        P(f"[{f}] {c} x{mult:g}: {g['label']} (bins with power {g['n_power']}/4, z > 2 in {g['n_kill']})")
        for x in g["rows"]:
            tw = x["terms_win"]
            P(f"    bin {x['bin']} (log M* {x['lm']}, n {x['n']}, r {x['r_kpc'][0]:.0f}-{x['r_kpc'][-1]:.0f} kpc): E {x['E']:+.3f} "
              f"(law sig {x['sig_law']:.3f}), W {x['W']:+.3f}, sig_tot {x['sig_win']:.3f}, line {x['line']:+.3f}, z {x['z']:+.2f} | "
              + " ".join(f"{k} {v:.3f}" for k, v in tw.items()) + f" | raw E {x['E_raw']:+.3f} W {x['W_raw']:+.3f}")

if not MUT:
    # M2: the law itself
    RES["M2"] = {}
    for f in FOOTS:
        rows = RES["grade"][f]["C1"]["rows"]; zl = [x["z_law"] for x in rows]
        ok = sum(1 for z in zl if z <= 2) >= 3
        RES["M2"][f] = dict(z_law=zl, E=[x["E"] for x in rows], sig=[x["sig_law"] for x in rows], pass_=bool(ok))
        P(f"M2 [{f}] the law: E_b " + ", ".join(f"{x['E']:+.3f}+-{x['sig_law']:.3f}" for x in rows)
          + f"; z_law " + ", ".join(f"{z:+.2f}" for z in zl) + f" -> {'PASS' if ok else 'FAIL'}")
    # M1 is graded in the twin; it is also computed here so the label can be stated in one place
    RES["M1"] = {}
    for f in FOOTS:
        labs = {c: grade(f, c, 4.0)["label"] for c in CELLS}
        RES["M1"][f] = dict(labels=labs, pass_=bool(all(v == "KILL HOLDS" for v in labs.values())))
        P(f"M1 [{f}] window x4: {labs} -> {'BITES' if RES['M1'][f]['pass_'] else 'DOES NOT BITE'}")
    # reported: all radii, projected reading
    RES["all_radii"] = {}; RES["projected"] = {}
    for f in FOOTS:
        RES["all_radii"][f] = {}; RES["projected"][f] = {}
        for c in CELLS:
            g = grade(f, c, 1.0, selname="all"); RES["all_radii"][f][c] = dict(label=g["label"], rows=[{k: x[k] for k in ("bin", "n", "E", "W", "sig_win", "z")} for x in g["rows"]])
            pr = projected(f, c, 1.0); RES["projected"][f][c] = pr
            P(f"reported [{f}] {c}: all radii {g['label']} (z " + ", ".join(f"{x['z']:+.2f}" for x in g["rows"]) + "); projected E/W "
              + ", ".join(f"{x['E']:+.3f}/{x['W']:+.3f}" for x in pr))
    # labels per footing
    RES["label"] = {}
    for f in FOOTS:
        labs = [RES["grade"][f][c]["label"] for c in CELLS]
        if "KILL SOFTENS" in labs: L = "KILL SOFTENS"
        elif all(l == "KILL HOLDS" for l in labs): L = "KILL HOLDS"
        elif all(l == "NO POWER" for l in labs): L = "NO POWER"
        else: L = "KILL HOLDS (cells with power) / NO POWER (others)"
        ctrl = RES["KA1"]["pass_"] and RES["KA2"]["pass_"] and RES["KA3"]["pass_"] and RES["M1"][f]["pass_"] and RES["M2"][f]["pass_"]
        RES["label"][f] = L if ctrl else f"NO VERDICT (control failed; reading {L})"
        P(f"LABEL [{f}]: {RES['label'][f]}  (cells: {dict(zip(CELLS, labs))})")

RES["seconds"] = time.time() - T0
try:
    import resource; RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
except Exception: pass
P(f"[{RES['seconds']:.0f} s, peak RSS {RES.get('peak_rss_GB', float('nan')):.2f} GB]")
P("kappa = 1/2 FITTED; not theory closed.")
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items() if k != "m"}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
