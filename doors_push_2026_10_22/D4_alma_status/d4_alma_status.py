#!/usr/bin/env python3
"""D4_alma_status: honest power of the two sealed ALMA tests under their GOVERNING plans (CFG806-U4, CFG809-GS4), from sealed
numbers only. Criteria: FROZEN_CRITERIA.md in this directory (committed alone first).
  python3 -B d4_alma_status.py            -> d4_alma_status.out, d4_alma_status_results.json
  D4_MUTATE=1 python3 -B d4_alma_status.py -> *_MUTATE.out, *_results_MUTATE.json (drops the M* term of sigma_Dv; K4 must fail)
Reads, never edits: the CFG571 seal (nu_mono), AG4e (n=1) and AG4d (n=2) seals, CFG571's functions (head, via the CFG942 harness
helper), the CFG942 GS4 delta_v (read-only import) and CFG942's committed R7 forecast JSONs (quoted as external inputs).
kappa = 1/2 FITTED; footings never pooled; one disc = a demonstration, no exclusion; not theory closed. No network."""
import os, sys, json, math, hashlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
H942 = os.path.join(REPO, "campaign_fresh_gravity", "CFG942_alma_scoring_readiness")
sys.path.insert(0, H942)
MUT = os.environ.get("D4_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
LINES = []; CHECKS = []
def P(s=""): LINES.append(s); print(s)
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
def sha(p): return hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()

SEALS = {"nu_mono": ("campaign_fresh_gravity/CFG571_prereg_proprietary_alma/cfg571_prereg_results.json",
                     "campaign_fresh_gravity/CFG571_prereg_proprietary_alma/PREDICTIONS_HASH.txt"),
         "n=1": ("argon_push/AG4e_n1_alma_seal/SEALED_N1.json", "argon_push/AG4e_n1_alma_seal/PREDICTIONS_HASH.txt"),
         "n=2": ("argon_push/AG4d_n2_alma_seal/SEALED_N2.json", "argon_push/AG4d_n2_alma_seal/PREDICTIONS_HASH.txt")}
WATCH = [v[0] for v in SEALS.values()] + [v[1] for v in SEALS.values()] + [
    "campaign_fresh_gravity/CFG806_u4_27928_scoring/FROZEN_CRITERIA.md", "campaign_fresh_gravity/CFG809_gs4_24110_ci21_scoring/FROZEN_CRITERIA.md",
    "campaign_fresh_gravity/CFG571_prereg_proprietary_alma/cfg571_prereg.py"]
snap0 = {p: sha(p) for p in WATCH}

import cfg942_common as C
import cfg942_gs4 as G4
P("D4_alma_status: ALMA honest power under the governing plans (CFG806-U4 1bf70683b, CFG809-GS4 966d50a87)" + (" [MUTATE]" if MUT else ""))
P("kappa = 1/2 FITTED; footings never pooled; one disc = demonstration, no exclusion; not theory closed.")
res = dict(mutate=MUT)

# ---------------------------------------------------------------- K1 seal hashes
ok = True; hs = {}
for k, (p, hp) in SEALS.items():
    h = sha(p); want = open(os.path.join(REPO, hp)).read().split()[0] if k != "nu_mono" else C.SEAL_HASH_EXPECT
    if k == "nu_mono": assert want in open(os.path.join(REPO, hp)).read()
    hs[k] = h; ok &= (h == want)
check("K1 seal sha256 (nu_mono, n=1, n=2) equal their hash files", ok, " ".join(f"{k}:{v[:8]}" for k, v in hs.items()), "exact")
res["seal_sha256"] = hs
S = {k: json.load(open(os.path.join(REPO, p))) for k, (p, _) in SEALS.items()}
S["nu_mono"] = S["nu_mono"]["results"]

# ---------------------------------------------------------------- K2 plan tables vs seal
r1, w1, b1 = C.transcription("campaign_fresh_gravity/CFG806_u4_27928_scoring/FROZEN_CRITERIA.md", "U4_27928")
r2, w2, b2 = C.transcription("campaign_fresh_gravity/CFG809_gs4_24110_ci21_scoring/FROZEN_CRITERIA.md", "GS4_24110")
check("K2 CFG806 s2 and CFG809 s2 tables equal the CFG571 seal", (not b1) and (not b2) and r1 > 0 and r2 > 0,
      f"rows {r1}+{r2} worst {max(w1, w2):.4f}", "<= 0.005 dex, FLOOR identical")

# ---------------------------------------------------------------- K3 CFG571 functions reproduce a sealed number
NS = C.load_cfg571(); geo = C.u4_geometry()
rr = C.predict(NS, geo["R"], 250.0, geo["z"], geo["lmstar"], geo["Rd"])["canon 9.36e-11|F-DESI"]["logMgas_Rg=Rd"]
d3 = abs(rr - S["nu_mono"]["U4_27928"]["250"]["canon 9.36e-11|F-DESI"]["logMgas_Rg=Rd"])
check("K3 CFG571 head recomputes U4 V_c 250 canon F-DESI Rg=Rd", d3 <= 1e-9, f"{d3:.1e}", "<= 1e-9 dex")

FOOTS = C.FOOTS; FW = ("F-DESI", "F-flat"); SH = ("Rg=Rd", "Rg=1.5Rd")
SIG_FLOOR = math.hypot(0.15, 0.15)
res["sigma_floor_U4"] = SIG_FLOOR

# ---------------------------------------------------------------- P1: U4 separations (CFG806 s4 statistic)
VG = ("225", "250", "275", "300")
def g_u4(kern, V, key, sh):
    d = S[kern]["U4_27928"][V][key]; return d["logMgas_" + sh]   # FLOOR <=> None (the seals store "floor" as a string)
def slope(kern, V, key, sh):
    grid = ["150", "175", "200", "225", "250", "275", "300"]; i = grid.index(V)
    pts = [(float(grid[j]), g_u4(kern, grid[j], key, sh)) for j in (i - 1, i, i + 1) if 0 <= j < len(grid)]
    pts = [(v, g) for v, g in pts if g is not None]
    if len(pts) < 2: return None
    (v0, g0), (v1, g1) = pts[0], pts[-1]; return (g1 - g0) / (v1 - v0)
def z_u4(gA, gB, sA, sB):
    z0 = abs(gA - gB) / SIG_FLOOR
    z5 = abs(gA - gB) / math.sqrt(SIG_FLOOR ** 2 + (5 * (sA or 0)) ** 2 + (5 * (sB or 0)) ** 2)
    return z0, z5
P("\n=== P1 U4_27928 (CFG806 s4: sigma_tot = 0.15 (+) 0.15 = %.3f dex with ZERO flux noise; z5 adds a 5 km/s V_c error via the sealed grid slope) ===" % SIG_FLOOR)
u4 = {}
for kern in ("nu_mono", "n=1", "n=2"):
    for f in FOOTS:
        for sh in SH:
            for V in VG:
                rh = g_u4(kern, V, f"{f}|R-H", sh)
                for m in FW:
                    gm = g_u4(kern, V, f"{f}|{m}", sh); k = f"{kern}|{f}|{sh}|{V}|{m} vs R-H"
                    if gm is None or rh is None:
                        u4[k] = dict(status="FLOOR " + ("framework" if gm is None else "") + (" R-H" if rh is None else "")); continue
                    z0, z5 = z_u4(gm, rh, slope(kern, V, f"{f}|{m}", sh), slope(kern, V, f"{f}|R-H", sh))
                    u4[k] = dict(dg=gm - rh, z0=z0, z5=z5)
for f in FOOTS:
    for sh in SH:
        for V in VG:
            for m in FW:
                a, b = g_u4("n=1", V, f"{f}|{m}", sh), g_u4("n=2", V, f"{f}|{m}", sh); k = f"n=1 vs n=2|{f}|{sh}|{V}|{m}"
                if a is None or b is None:
                    u4[k] = dict(status="FLOOR " + ("n=1" if a is None else "") + (" n=2" if b is None else "")); continue
                z0, z5 = z_u4(a, b, slope("n=1", V, f"{f}|{m}", sh), slope("n=2", V, f"{f}|{m}", sh))
                u4[k] = dict(dg=b - a, z0=z0, z5=z5)
for k, v in u4.items():
    if k.split("|")[2] == "Rg=Rd":
        P(f"  {k}: " + (v["status"] if "status" in v else f"dlogM {v['dg']:+.3f}  z_noisefree {v['z0']:.2f}  z(5 km/s) {v['z5']:.2f}"))
P("  (Rg=1.5Rd rows are in the JSON.)")
res["U4"] = u4
# P1b: nu_mono above the sealed grid, recomputed with CFG571's functions exactly as CFG806 s2 prescribes (KMOS3D integrated
# H-alpha sigma 224.5 km/s hints V_c > 300; CFG942 README). Noise-free z only.
P("  nu_mono above the sealed grid (CFG571 functions, CFG806 s2 recompute rule), Rg=Rd, noise-free z F-DESI vs R-H:")
hi = {}
for f in FOOTS:
    for V in (325.0, 350.0, 400.0):
        r = C.predict(NS, geo["R"], V, geo["z"], geo["lmstar"], geo["Rd"])
        a, b = r[f"{f}|F-DESI"]["logMgas_Rg=Rd"], r[f"{f}|R-H"]["logMgas_Rg=Rd"]
        hi[f"{f}|{V:.0f}"] = None if (a is None or b is None) else abs(a - b) / SIG_FLOOR
        P(f"    {f} V_c {V:.0f}: z {hi[f'{f}|{V:.0f}']:.2f}" if hi[f"{f}|{V:.0f}"] is not None else f"    {f} V_c {V:.0f}: FLOOR")
res["U4_above_grid_nu_mono_z"] = hi
# P1c (information; CLARIFICATION A-U15 keeps the M* 0.2 dex systematic OUT of the required range): what the 0.2 dex M*
# systematic (CFG806 s3.2) does to the required GAS when propagated, nu_mono, Rg=Rd. d_M = half the change of log M_gas,req
# between M* -0.2 and +0.2 dex (CFG571 functions). FLOOR at an end => the requirement is unbounded there (reported).
P("  M* +-0.2 dex propagated into the required gas (information; A-U15 keeps it out of the verdict), nu_mono, Rg=Rd:")
pm = {}
for f in FOOTS:
    for V in (250.0, 275.0, 300.0):
        e = {}
        for m in ("F-DESI", "R-H"):
            lo = C.predict(NS, geo["R"], V, geo["z"], geo["lmstar"] - 0.2, geo["Rd"])[f"{f}|{m}"]["logMgas_Rg=Rd"]
            h_ = C.predict(NS, geo["R"], V, geo["z"], geo["lmstar"] + 0.2, geo["Rd"])[f"{f}|{m}"]["logMgas_Rg=Rd"]
            c0 = C.predict(NS, geo["R"], V, geo["z"], geo["lmstar"], geo["Rd"])[f"{f}|{m}"]["logMgas_Rg=Rd"]
            e[m] = dict(req=c0, at_minus=lo, at_plus=h_, dM=None if (lo is None or h_ is None) else 0.5 * abs(lo - h_))
        a, b = e["F-DESI"], e["R-H"]
        if None in (a["req"], b["req"]): z = None; why = "FLOOR at nominal M*"
        elif a["dM"] is None or b["dM"] is None: z = 0.0; why = "a model is FLOOR at M*+0.2: its requirement reaches zero gas, separation not bounded away from 0"
        else: z = abs(a["req"] - b["req"]) / math.sqrt(SIG_FLOOR ** 2 + a["dM"] ** 2 + b["dM"] ** 2); why = ""
        pm[f"{f}|{V:.0f}"] = dict(F_DESI=a, R_H=b, z_with_Mstar=z, note=why)
        r2 = lambda x: "FLOOR" if x is None else "%.2f" % x
        P(f"    {f} V_c {V:.0f}: F-DESI req {r2(a['req'])} (M*-0.2: {r2(a['at_minus'])}, +0.2: {r2(a['at_plus'])}); R-H req {r2(b['req'])} "
          f"(M*-0.2: {r2(b['at_minus'])}, +0.2: {r2(b['at_plus'])}) -> z {('%.2f' % z) if z is not None else 'n/a'} {why}")
res["U4_Mstar_propagated"] = pm

# ---------------------------------------------------------------- P2: GS4 separations (CFG809 s4 statistic)
RE, RD, Gc = G4.RE, G4.RD, 4.30091e-6
def vreq2(kern, lm, key): return 10 ** S[kern]["GS4_24110"][lm][key]["logVbar2R_G"] * Gc / RE
def floor(kern, lm, key, dm=0.0): return vreq2(kern, lm, key) - G4.v2s(float(lm) + dm) <= 0
def dv_own(kern, lm, key, g, Rg):
    vr = vreq2(kern, lm, key); sg = math.hypot(0.0, 0.2); lmf = float(lm)
    f = lambda dg, dm: math.log10((G4.v2s(lmf + dm) + G4.v2g(g + dg, Rg)) / vr)
    sM = 0.0 if MUT else 0.5 * (f(0, 0.2) - f(0, -0.2))
    return f(0, 0), 0.5 * math.hypot(f(sg, 0) - f(-sg, 0), 2 * sM)
# K4: own statistic == harness delta_v on every nu_mono pair
worst = 0.0; npair = 0
for lm in ("10.89", "10.76"):
    for f in FOOTS:
        for sh in SH:
            Rg = RD * (1.0 if sh == "Rg=Rd" else 1.5)
            for mA in C.MODELS:
                gA = S["nu_mono"]["GS4_24110"][lm][f"{f}|{mA}"]["logMgas_" + sh]
                if gA is None: continue
                for mB in C.MODELS:
                    h = G4.delta_v(dict(logMgas=gA, sig_flux_dex=0.0, detected=True), f"{f}|{mB}", float(lm), Rg)
                    D, s = dv_own("nu_mono", lm, f"{f}|{mB}", gA, Rg)
                    worst = max(worst, abs(D - h["Delta"]), abs(s - h["sigma"])); npair += 1
check("K4 lane Delta_v and sigma_Dv equal cfg942_gs4.delta_v on every nu_mono pair", worst <= 1e-12 and npair > 0, f"{worst:.1e} over {npair}", "<= 1e-12")

P("\n=== P2 GS4_24110 (CFG809 s4: gas = model A's sealed need, detected, flux error 0; z = |Delta_v(B)| / sigma_Dv(B); sigma = gas route 0.2 (+) M* 0.2 dex) ===")
gs = {}
def pair(kA, mA, kB, mB, lm, f, sh, lab):
    Rg = RD * (1.0 if sh == "Rg=Rd" else 1.5)
    gA = S[kA]["GS4_24110"][lm][f"{f}|{mA}"]["logMgas_" + sh]
    if gA is None: return dict(status=f"A FLOOR ({kA} {mA}): no gas allowed, pair undefined")
    D, s = dv_own(kB, lm, f"{f}|{mB}", gA, Rg); out = dict(gas=gA, Delta_v=D, sigma=s, z=abs(D) / s)
    if floor(kB, lm, f"{f}|{mB}"):
        out.update(B_floor=True, floor_persists_Mstar_minus_0p2=floor(kB, lm, f"{f}|{mB}", -0.2))
    return out
for lm in ("10.89", "10.76"):
    for f in FOOTS:
        for sh in SH:
            for kern in ("nu_mono", "n=1", "n=2"):
                for m in FW:
                    gs[f"{kern}|{lm}|{f}|{sh}|gas={m} need, scored R-H"] = pair(kern, m, kern, "R-H", lm, f, sh, "")
            for m in FW:
                gs[f"n=1 vs n=2|{lm}|{f}|{sh}|gas=n1 {m}, scored n2 {m}"] = pair("n=1", m, "n=2", m, lm, f, sh, "")
                gs[f"n=1 vs n=2|{lm}|{f}|{sh}|gas=n2 {m}, scored n1 {m}"] = pair("n=2", m, "n=1", m, lm, f, sh, "")
for k, v in gs.items():
    if k.split("|")[3] == "Rg=Rd":
        if "status" in v: P(f"  {k}: {v['status']}")
        else: P(f"  {k}: gas {v['gas']:.2f}  Delta_v {v['Delta_v']:+.3f} / {v['sigma']:.3f} = z {v['z']:.2f}" +
                (f"  [B FLOOR; persists at M*-0.2: {v['floor_persists_Mstar_minus_0p2']}]" if v.get("B_floor") else ""))
P("  (Rg=1.5Rd rows are in the JSON.)")
res["GS4"] = gs

# ---------------------------------------------------------------- summary of P1/P2 (frozen readings R-POWER, R-FLOOR)
def mx(d, pre):
    vals = [(v.get("z0", v.get("z")), k) for k, v in d.items() if k.startswith(pre) and "status" not in v and not v.get("B_floor")]
    return max(vals) if vals else (None, None)
summ = {}
for lab, d, pre in (("U4 framework vs R-H, nu_mono (governing kernel)", u4, "nu_mono|"), ("U4 framework vs R-H, n=1", u4, "n=1|"),
                    ("U4 framework vs R-H, n=2", u4, "n=2|"), ("U4 n=1 vs n=2", u4, "n=1 vs n=2|"),
                    ("GS4 framework vs R-H, nu_mono (non-FLOOR R-H only)", gs, "nu_mono|"), ("GS4 framework vs R-H, n=1 (non-FLOOR)", gs, "n=1|"),
                    ("GS4 framework vs R-H, n=2 (non-FLOOR)", gs, "n=2|"), ("GS4 n=1 vs n=2", gs, "n=1 vs n=2|")):
    z, k = mx(d, pre); summ[lab] = dict(max_z_noisefree=z, branch=k, reaches_3sigma=(z is not None and z >= 3))
z5max = max((v["z5"], k) for k, v in u4.items() if "z5" in v)
fl = [(k, v) for k, v in gs.items() if v.get("B_floor") and k.startswith("nu_mono|")]
summ["GS4 nu_mono R-H FLOOR rows (rule-based tension)"] = dict(n=len(fl), persists_at_Mstar_minus_0p2=sum(v["floor_persists_Mstar_minus_0p2"] for _, v in fl),
                                                              max_Delta_v_alone_z=max(v["z"] for _, v in fl) if fl else None)
summ["U4 max z with 5 km/s V_c error"] = dict(z=z5max[0], branch=z5max[1])
P("\n=== SUMMARY (noise-free ceilings; the frozen reading R-POWER) ===")
for k, v in summ.items(): P(f"  {k}: {v}")
anyz = [v for k, v in summ.items() if "reaches_3sigma" in v and v["reaches_3sigma"]]
P(f"  ANY pair >= 3 sigma on either disc (noise-free, non-FLOOR): {'YES: ' + str(anyz) if anyz else 'NO'}")
res["summary"] = summ; res["any_3sigma"] = bool(anyz)

# ---------------------------------------------------------------- P3 sensitivity (CFG942 R7, committed; external input)
fu = json.load(open(os.path.join(H942, "cfg942_u4_selftest_results.json")))["results"]["forecast"]
fg = json.load(open(os.path.join(H942, "cfg942_gs4_selftest_results.json")))["results"]["forecast"]
P("\n=== P3 G1 S/N at native resolution for the required gas (CFG942 R7, committed selftest JSONs; archive metadata not re-verified) ===")
for k, v in list(fu.items()) + list(fg.items()): P(f"  {k}: log M_gas {v['logMgas']:.2f}; " + "; ".join(v["cells"]))
res["R7_quoted"] = dict(U4=fu, GS4=fg)

# ---------------------------------------------------------------- P4 record checks
P("\n=== P4 record checks ===")
gov = ["campaign_fresh_gravity/CFG806_u4_27928_scoring/" + x for x in sorted(os.listdir(os.path.join(REPO, "campaign_fresh_gravity/CFG806_u4_27928_scoring")))] + \
      ["campaign_fresh_gravity/CFG809_gs4_24110_ci21_scoring/" + x for x in sorted(os.listdir(os.path.join(REPO, "campaign_fresh_gravity/CFG809_gs4_24110_ci21_scoring")))]
tok = ("AG4d", "AG4e", "SEALED_N1", "SEALED_N2", "n=1", "n=2", "nu1", "ν₁", "ν_1")
hits = {p: [t for t in tok if t in open(os.path.join(REPO, p)).read()] for p in gov if p.endswith(".md")}
named = {p: h for p, h in hits.items() if h}
P(f"  (a) governing plan files that name the n=1/n=2 seals: {named if named else 'NONE'} (of {len(hits)} files)")
can = open(os.path.join(REPO, "campaign_fresh_gravity/THEORY_CANONICAL_2026-10-21_DRAFT.md")).read()
law_n1 = "g_N = g²/(g + a0)" in can
P(f"  (b) canonical draft s1 law 'g_N = g²/(g + a0)' (= n=1, AG4e kernel): {law_n1}; governing plans score the CFG571 seal, kernel nu_mono")
tops = {k: max(int(x) for x in S[k]["U4_27928"]) for k in S}
P(f"  (c) U4 sealed V_c grid top: {tops} km/s; CFG806 recomputes nu_mono at any measured V_c; no governing rule reads n=1/n=2 at all")
rel = {}
d570 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity/CFG570_alma_z12_20_window/cfg570_alma_window_results.json")))["results"]
for t, line, prop in (("U4_27928", "CO(2-1)", "2024.1.00100.L"), ("GS4_24110", "[CI](2-1)", "2025.1.01377.L")):
    rel[t] = sorted({r["release"] for r in d570[t]["lines"] if r["line"] == line and r["proposal"] == prop})
check("K5 CFG570 release dates equal the plans' dates", rel == {"U4_27928": ["2026-11-06"], "GS4_24110": ["2026-11-28"]}, rel, "U4 2026-11-06, GS4 2026-11-28")
fits_hits = []
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in (".git", ".claude", "node_modules")]
    for fn in files:
        if fn.lower().endswith((".fits", ".fits.gz", ".fits.fz", ".ms", ".tgz", ".tar")) and any(s in fn for s in ("2024.1.00100", "2025.1.01377", "U4_27928", "27928", "GS4_24110", "24110")):
            fits_hits.append(os.path.relpath(os.path.join(root, fn), REPO))
P(f"  (e) data files on disk for either programme/target: {fits_hits if fits_hits else 'NONE'}")
res["record"] = dict(governing_files_naming_n1_n2=named, canonical_law_is_n1=law_n1, U4_grid_top=tops, release=rel, data_on_disk=fits_hits)

snap1 = {p: sha(p) for p in WATCH}
check("K6 no frozen or sealed file changed during the run", snap0 == snap1, f"{len(WATCH)} files", "sha256 identical")
npass = sum(ok for _, ok in CHECKS)
P(f"\nD4_ALMA_STATUS COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
res["checks"] = CHECKS
open(os.path.join(HERE, f"d4_alma_status{SUF}.out"), "w").write("\n".join(LINES) + "\n")
json.dump(res, open(os.path.join(HERE, f"d4_alma_status_results{SUF}.json"), "w"), indent=1, default=str)
sys.exit(0 if npass == len(CHECKS) else 1)
