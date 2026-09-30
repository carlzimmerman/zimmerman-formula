"""CFG236 main: attack (a) reproduction of CFG198 (R198) and CFG199 (R199, needs the external .dat files), pass lines of section 6.
Exit 0.  Env: CFG236_SUFFIX (output suffix, e.g. _seed237), SEED (default 236), B (default 10000), NODAT=1 to skip [DAT] rows."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG236_common as c

SEED = int(os.environ.get("SEED", "236"))
B = int(os.environ.get("B", "10000"))
USE_DAT = c.dat_available() and os.environ.get("NODAT") != "1"
o = c.Out("main")
c.header(o, "CFG236 main: reproduction of CFG198 / CFG199")
o.P(f"seed {SEED}, B {B}, [DAT] rows {'ON' if USE_DAT else 'OFF'}")
PL = []


def line(pid, desc, mine, target, tol, info=False):
    ok = (abs(mine - target) <= tol) if np.isfinite(mine) else False
    PL.append(dict(id=pid, desc=desc, mine=mine, target=target, tol=tol, ok=bool(ok), info=info))
    o.P(f"{'INFO ' if info else ''}{'PASS' if ok else 'FAIL'} {pid}: {desc}: mine {mine:+.4f}  target {target:+.4f}  (tol {tol})")


def lineN(pid, desc, mine, target):
    ok = (mine == target)
    PL.append(dict(id=pid, desc=desc, mine=mine, target=target, tol=0, ok=bool(ok), info=False))
    o.P(f"{'PASS' if ok else 'FAIL'} {pid}: {desc}: mine {mine}  target {target}")


T = c.load_numeric()
idx, cnt = c.sample(T)
o.P("sample chain:", cnt)
lineN("N1", "rows", cnt["n_rows"], 126)
lineN("N2", "finite", cnt["n_finite"], 124)
lineN("N3", "bulge among the 124", cnt["bulge_in_finite"], 14)
lineN("N3b", "bulge among all 126", cnt["bulge_all"], 15)
lineN("N4", "disc-only", cnt["n_disc"], 110)
lineN("N5", "S (0<fDM<1)", cnt["n_S"], 109)
C = c.get_cols(T, idx)
z = C["z"]
zmed = float(np.median(z))
o.P(f"S: z range {z.min():.3f}-{z.max():.3f}, median {zmed:.3f}; logM*_SED median {np.median(C['logMsed']):.2f}")

# ---- added controls (sanity, not in the frozen text)
yy = np.linspace(0.05, 40, 400000)
h = c.y2_term(yy)   # y = R/(2Rd)
Rd_ratio = 2 * yy[np.argmax(h)]
vmax = 2 * h.max()  # v^2 Rd/(GM) = 2 y^2 [..]
o.P(f"C1 disc: peak at R/Rd = {Rd_ratio:.3f}; v2max Rd/(GM) = {vmax:.4f}")
yk = 25.0
o.P(f"C1 disc: at R=50 Rd, v^2 R/(GM) = {2*50*c.y2_term(yk):.4f}  (should be ~1)")  # v2 R/(GM) = (2/Rd) y2 * R /... R=50Rd -> 2*y2*50
kb = {}
for kn in ("RAR", "P2"):
    Ds = np.geomspace(1.06, 100, 200)
    ker = c.get_kernel(kn)
    ys = c.invert(Ds, ker)
    kb[kn] = float(np.max(np.abs(ker(ys) / Ds - 1)))
o.P(f"C2 kernel round trip (max rel err): {kb}")
# C3 route identity (R198): M*_SED := M_fit, mu := 0
C_id = dict(C)
C_id["logMsed"] = C["logMfit"]
Rid = c.routes(C_id, dict(mu_scale=0.0))
okid = all(np.nanmax(np.abs(np.log(Rid["a0_" + r] / Rid["a0_i"]))) < 1e-12 for r in ("ii", "iii"))
o.P(f"C3 route identity (R198): {'PASS' if okid else 'FAIL'}")
# C4 interpolation synthetic
A = np.zeros((25, 5)); r = np.linspace(-3, 3, 25); A[:, 1] = r; A[:, 3] = 40 * r
A[:, 3][r == 0] = 0
vv = c.at_radius(A, 1.0, 3)
o.P(f"C4 interpolation: {vv:.12f} (expect 40) err {abs(vv-40):.1e}")

# ---- hash verification of the external data
hv = None
if USE_DAT:
    hv = c.verify_hashes()
    o.P("hash verification of external files vs the repo manifests:", {k: v for k, v in hv.items() if k != "bad"}, hv["bad"][:3])
    o.res["hash"] = hv
    if hv["n_bad"] or hv["n_missing"] or hv["cat_bad"]:
        o.P("ABORT: hash mismatch"); o.finish(); sys.exit(0)

# ---- P1: drift
mu = c.mu_mol(z, C["logMsed"])
d_star = C["logMfit"] - C["logMsed"]
d_star_h2 = d_star - np.log10(1 + mu)
p1, bs1 = c.slope_table(z, dict(dstar=d_star, dstar_h2=d_star_h2), B, SEED)
o.P(f"P1 drift (n={len(z)}): Delta* slope {p1['dstar']['b']:+.3f} [{p1['dstar']['lo']:+.3f},{p1['dstar']['hi']:+.3f}] median {np.median(d_star):+.3f}")
o.P(f"P1 drift: Delta*-log(1+mu) slope {p1['dstar_h2']['b']:+.3f} [{p1['dstar_h2']['lo']:+.3f},{p1['dstar_h2']['hi']:+.3f}] median {np.median(d_star_h2):+.3f}")
line("T1", "Delta* slope", p1["dstar"]["b"], -0.723, 0.03)
line("T1m", "Delta* median", float(np.median(d_star)), -0.112, 0.01)
line("T1lo", "Delta* CI lo", p1["dstar"]["lo"], -0.966, 0.05, True)
line("T1hi", "Delta* CI hi", p1["dstar"]["hi"], -0.498, 0.05, True)
line("T2", "Delta*-log(1+mu) slope", p1["dstar_h2"]["b"], -0.868, 0.03)
line("T2m", "Delta*-log(1+mu) median", float(np.median(d_star_h2)), -0.512, 0.03)
line("T2lo", "CI lo", p1["dstar_h2"]["lo"], -1.107, 0.05, True)
line("T2hi", "CI hi", p1["dstar_h2"]["hi"], -0.616, 0.05, True)
o.P(f"slope of log10(1+mu) = {p1['dstar']['b']-p1['dstar_h2']['b']:+.3f} (target 0.145)")
o.res["P1"] = p1


# ---- R198 main + robustness
def run198(cfg, label, B_=B, seed=SEED):
    R = c.routes(C, cfg)
    cols = {r: np.log10(R["a0_" + r]) for r in ("i", "ii", "iii")}
    pairs = {"d_ii_i": ("i", "ii"), "d_iii_i": ("i", "iii")}
    st, bs = c.slope_table(z, cols, B_, seed, pairs)
    refs = {}
    for r in ("i", "ii", "iii"):
        m = np.isfinite(cols[r])
        refs[r] = c.ref_slopes(z[m])
    o.P(f"[{label}]")
    for r in ("i", "ii", "iii"):
        s = st[r]
        cl = c.outside_set(s, refs[r])
        o.P(f"   route ({r}): n={s['n']}  b={s['b']:+.3f} [{s['lo']:+.3f},{s['hi']:+.3f}] sd {s['sd']:.3f}  excludes: {cl if cl else 'none'}")
    for k in ("d_ii_i", "d_iii_i"):
        s = st[k]
        o.P(f"   paired {k}: n={s['n']}  {s['b']:+.3f} [{s['lo']:+.3f},{s['hi']:+.3f}]")
    return R, cols, st, refs, bs


R, cols, st, refs, bs = run198({}, "R198 primary (nu_RAR, fitted Sigma_HI, mu x1)")
o.res["R198_primary"] = dict(st=st, refs=refs)
lineN("N6", "n route (i)", st["i"]["n"], 108)
lineN("N7", "n route (ii)", st["ii"]["n"], 85)
lineN("N8", "n route (iii)", st["iii"]["n"], 99)
lineN("N9", "paired (ii-i)", st["d_ii_i"]["n"], 84)
lineN("N10", "paired (iii-i)", st["d_iii_i"]["n"], 98)
zh = z <= zmed
cens = ~np.isfinite(R["a0_ii"])
lineN("N11", "D<=1.05 route (ii) low-z half", int(np.sum(cens & zh)), 9)
lineN("N12", "D<=1.05 route (ii) high-z half", int(np.sum(cens & ~zh)), 15)
line("T3", "b_i (R198)", st["i"]["b"], 0.789, 0.05)
line("T4", "b_ii (R198)", st["ii"]["b"], -0.041, 0.05)
line("T5", "b_iii (R198)", st["iii"]["b"], 0.075, 0.05)
line("T6", "paired Delta b (ii-i)", st["d_ii_i"]["b"], -0.939, 0.05)
line("T6b", "paired b_iii - b_i", st["d_iii_i"]["b"], -0.693, 0.05)
for k, tg in (("i", (0.514, 1.071)), ("ii", (-0.467, 0.360)), ("iii", (-0.233, 0.349)), ("d_ii_i", (-1.261, -0.633)), ("d_iii_i", (-0.931, -0.480))):
    line(f"T-CI-{k}-lo", "CI lo", st[k]["lo"], tg[0], 0.05, True)
    line(f"T-CI-{k}-hi", "CI hi", st[k]["hi"], tg[1], 0.05, True)
rf = c.ref_slopes(z)
o.P(f"reference slopes over S: flat 0, E(z) {rf['Ez']:+.4f}, III {rf['III']:+.4f}")
line("T7a", "E(z) reference slope", rf["Ez"], 0.258, 0.005)
line("T7b", "III-law reference slope", rf["III"], 0.298, 0.005)
o.P("R1 (route ii): excluded =", c.outside_set(st["ii"], refs["ii"]), " classification:", c.classify(st["ii"], refs["ii"]))
o.P("R0 (route i): excluded =", c.outside_set(st["i"], refs["i"]))
# levels z-thirds (route (i) galaxies)
vi = np.isfinite(R["a0_i"])
th = c.thirds(z[vi])
ids_i = np.where(vi)[0]
lev = {}
for r in ("i", "ii", "iii"):
    L = c.level_log(R["a0_" + r])
    lev[r] = [float(np.nanmedian(L[ids_i[t]])) for t in th]
    o.P(f"level (R198, z-thirds of route-(i) galaxies; median log10 a0): route ({r}) {['%.2f' % v for v in lev[r]]}")
o.P(f"footings {c.LOG_CAN:.3f} / {c.LOG_ALT:.3f}; median z of lowest third {np.median(z[ids_i[th[0]]]):.3f}")
line("T9i", "level low third route (i)", lev["i"][0], -9.65, 0.05)
line("T9ii", "level low third route (ii)", lev["ii"][0], -9.69, 0.05)
line("T9iii", "level low third route (iii)", lev["iii"][0], -9.38, 0.05)
o.res["levels198"] = lev
# robustness rows
rob = {}
rows = [("Sig0", dict(Sig=0.0), dict(b_i=0.775, b_ii=-0.182, d=-1.111, out=["Ez", "III"])),
        ("Sig15", dict(Sig=15.0), dict(b_i=0.822, b_ii=0.106, d=-0.819, out=[])),
        ("mu0.5", dict(mu_scale=0.5), dict(b_i=0.789, b_ii=-0.011, d=-0.866, out=[])),
        ("mu2", dict(mu_scale=2.0), dict(b_i=0.789, b_ii=-0.202, d=-1.127, out=["III"]))]
for nm, cfg, tg in rows:
    Rr, cr, sr, rr, _ = run198(cfg, f"R198 robustness {nm}")
    ex = c.outside_set(sr["ii"], rr["ii"])
    rob[nm] = dict(st=sr, excluded=ex)
    line(f"T8-{nm}-bi", "b_i", sr["i"]["b"], tg["b_i"], 0.05)
    line(f"T8-{nm}-bii", "b_ii", sr["ii"]["b"], tg["b_ii"], 0.05)
    line(f"T8-{nm}-d", "Delta b", sr["d_ii_i"]["b"], tg["d"], 0.05)
    okc = sorted(ex) == sorted(tg["out"])
    PL.append(dict(id=f"R1-{nm}", desc=f"R1 excluded set {ex} vs {tg['out']}", ok=okc, info=False, mine=str(ex), target=str(tg["out"])))
    o.P(f"{'PASS' if okc else 'FAIL'} R1-{nm}: excluded {ex}, target {tg['out']}")
o.res["robust198"] = rob
o.P(f"R1-primary: excluded {c.outside_set(st['ii'], refs['ii'])} vs target []")
PL.append(dict(id="R1-primary", ok=c.outside_set(st["ii"], refs["ii"]) == [], info=False))
o.P(f"R1-route(iii): excluded {c.outside_set(st['iii'], refs['iii'])} vs target []")
PL.append(dict(id="R1-iii", ok=c.outside_set(st["iii"], refs["iii"]) == [], info=False))
# kernels
kres = {}
for kn in ("P2", "mono"):
    try:
        Rk = c.routes(C, dict(kernel=kn))
        ck = {r: np.log10(Rk["a0_" + r]) for r in ("i", "ii", "iii")}
        kres[kn] = {r: c.theil_sen(z, ck[r]) for r in ck}
        kres[kn]["d"] = kres[kn]["ii"] - kres[kn]["i"]
        o.P(f"kernel {kn}{' (IMPORT from CFG4_common, shared object)' if kn=='mono' else ''}: b_i {kres[kn]['i']:+.3f}, b_ii {kres[kn]['ii']:+.3f}, b_iii {kres[kn]['iii']:+.3f}")
    except Exception as e:
        o.P(f"kernel {kn}: NOT RUN ({type(e).__name__})")
if "mono" in kres:
    line("K-mono", "nu_mono (import) b_i within 0.005 of nu_RAR primary", kres["mono"]["i"], st["i"]["b"], 0.005)
    line("K-mono2", "nu_mono (import) b_ii within 0.005 of nu_RAR primary", kres["mono"]["ii"], st["ii"]["b"], 0.005)
o.res["kernels"] = kres
# decomposition b = 2 s_obs - s_bar (deep-regime identity)
for r in ("i", "ii", "iii"):
    s_obs = c.theil_sen(z, np.log10(R["gobs"]))
    s_bar = c.theil_sen(z, np.log10(R["gb_" + r]))
    o.P(f"decomposition route ({r}): slope log g_obs {s_obs:+.3f}, slope log g_bar {s_bar:+.3f}, 2 s_obs - s_bar {2*s_obs-s_bar:+.3f} vs b {st[r]['b']:+.3f}")

# ---- v22 style variant skipped (A3 unverified); R199 [DAT]
if USE_DAT:
    dat = c.load_dat(T, idx)
    o.P(f"v_f(R_e) median {np.median(dat['v1']):.1f} km/s; finite {int(np.isfinite(dat['v1']).sum())}/{len(z)}")
    R199 = {}
    inc = C["incl"]
    sini = np.sin(np.radians(inc))
    tg199 = {"a": dict(bi=0.65, bii=-0.20, d=-1.03, lev=-10.38, levci=(-10.71, -10.12), rho=0.40, s=0.84),
             "b": dict(bi=0.63, bii=-0.22, d=-1.03, lev=-10.14, levci=(-10.45, -9.94), rho=-0.01, s=0.75)}
    for rd in ("a", "b"):
        gp = c.gperp_reading(dat["v1"], C["Re"], inc, rd)
        Rr = c.routes(C, dict(mode="R199", gperp=gp))
        cr = {r: np.log10(Rr["a0_" + r]) for r in ("i", "ii", "iii")}
        sr, bsr = c.slope_table(z, cr, B, SEED, {"d_ii_i": ("i", "ii"), "d_iii_i": ("i", "iii")})
        rr = {r: c.ref_slopes(z[np.isfinite(cr[r])]) for r in cr}
        o.P(f"[R199 reading ({rd}), drift OFF]")
        for r in ("i", "ii", "iii"):
            s = sr[r]
            o.P(f"   route ({r}): n={s['n']} b={s['b']:+.3f} [{s['lo']:+.3f},{s['hi']:+.3f}] excludes {c.outside_set(s, rr[r]) or 'none'}")
        s = sr["d_ii_i"]
        o.P(f"   paired Delta b: n={s['n']} {s['b']:+.3f} [{s['lo']:+.3f},{s['hi']:+.3f}]")
        t = tg199[rd]
        line(f"T10{rd}-bi", "b_i", sr["i"]["b"], t["bi"], 0.05)
        line(f"T10{rd}-bii", "b_ii", sr["ii"]["b"], t["bii"], 0.05)
        line(f"T10{rd}-d", "Delta b", sr["d_ii_i"]["b"], t["d"], 0.05)
        vi2 = np.isfinite(Rr["a0_i"])
        th2 = c.thirds(z[vi2])
        ids2 = np.where(vi2)[0]
        L = c.level_log(Rr["a0_i"])
        low = L[ids2[th2[0]]]
        lo_, hi_ = c.boot_median(low, B, SEED)
        med = float(np.median(low))
        cls = "below both" if hi_ < c.LOG_CAN else ("above both" if lo_ > c.LOG_ALT else "consistent with footing(s)")
        o.P(f"   L1 level lowest third: {med:.2f} [{lo_:.2f},{hi_:.2f}] -> {cls}")
        line(f"T11{rd}", "level lowest third", med, t["lev"], 0.05)
        okcls = (cls == "below both") if rd == "a" else (cls != "below both" and cls != "above both")
        PL.append(dict(id=f"L1{rd}-class", ok=okcls, info=False, mine=cls, target="below both" if rd == "a" else "consistent"))
        o.P(f"{'PASS' if okcls else 'FAIL'} L1{rd}-class: {cls}")
        if rd == "b":
            o.P(f"   route (ii) CI upper edge {sr['ii']['hi']:+.4f} vs III slope {rr['ii']['III']:+.4f}: {'below (excludes III)' if sr['ii']['hi']<rr['ii']['III'] else 'not below'}")
        vc198 = np.sqrt(R["gobs"] * C["Re"])
        vperp = dat["v1"] / sini if rd == "b" else dat["v1"]
        rho_s = float(c.stats.spearmanr(vperp / vc198, sini)[0])
        share = 1 - (vperp ** 2 / C["Re"]) / R["gobs"]
        o.P(f"   L3: spearman(v_perp/v_c,198 , sin i) = {rho_s:+.2f}; share s median {np.median(share):.2f} [16-84: {np.percentile(share,16):.2f}, {np.percentile(share,84):.2f}]; median log10(g_perp/g_obs198) = {np.median(np.log10((vperp**2/C['Re'])/R['gobs'])):+.2f}")
        line(f"T12{rd}-rho", "rho with sin i", rho_s, t["rho"], 0.1)
        line(f"T12{rd}-s", "share s median", float(np.median(share)), t["s"], 0.03)
        R199[rd] = dict(st=sr, level=(med, lo_, hi_), rho=rho_s)
    o.res["R199"] = R199
    # CFG199 C4-like check: R198 primary from copied formulas is R198 itself (done above)

# ---- verdicts
npass = sum(1 for p in PL if p["ok"] and not p.get("info"))
nfail = [p["id"] for p in PL if not p["ok"] and not p.get("info")]
ninfo = [p["id"] for p in PL if not p["ok"] and p.get("info")]
o.P(f"\nPASS LINES: {npass} pass, {len(nfail)} fail (non-info); fails: {nfail}; info misses: {ninfo}")
o.res["pass_lines"] = PL
o.finish()
sys.exit(0)
