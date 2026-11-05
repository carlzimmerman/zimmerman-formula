#!/usr/bin/env python3
"""FA1 / I6, the Galileon-determinant selector, with a static field solve. Criteria FROZEN_CRITERIA.md (062648e489).
  python3 i6_galileon.py              -> i6_results.json, i6.out
  I6_MUTATE=1 python3 i6_galileon.py  -> i6_results_MUTATE.json, i6_MUTATE.out  (s -> -s on the galaxy side; must bite; no ladder)
Reads SPARC rotmod (CRG1 inputs) and Table 1, X-COP FITS (as FA1/RQ3). Solver in galsolve.py.
kappa = 1/2 FITTED; not theory closed. Adopts nothing; the cold sector stays retired."""
import os, sys, json, math, glob, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
import numpy as np
from scipy.optimize import brentq
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); FA1 = os.path.dirname(HERE); RB = os.path.dirname(FA1); REPO = os.path.dirname(RB)
sys.path.insert(0, HERE); import galsolve as gs
MUT = os.environ.get("I6_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; SIGN = -1.0 if MUT else 1.0
OUT = open(os.path.join(HERE, f"i6{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n")
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt")
G_SI, MSUN, KPC, C = 6.674e-11, 1.989e30, 3.0857e19, 2.99792458e8
F_MAX = (0.110 ** 2 - 0.069 ** 2) / 0.40 ** 2; D_DUST = 1.5; RMS_LINE = math.sqrt(0.110 ** 2 - 0.069 ** 2)
CHECKS = {}; RES = dict(criteria="062648e489", mutate=MUT, D=D_DUST, rms_line=RMS_LINE, f_max=F_MAX)
def check(n, ok, d):
    CHECKS[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
def kfac(a0): return C ** 2 / (3 * a0 ** 2)                      # k = r_c^2/(3 c^2), r_c = c^2/a0  [s^2]
def dpi_phys(r, M, a0):
    """pi' (m/s^2) from r^2 pi' + 2 k r pi'^2 = 2 G M (SI)"""
    k = kfac(a0); r = np.asarray(r, float); M = np.asarray(M, float)
    return (-r * r + np.sqrt(r ** 4 + 16 * k * r * G_SI * M)) / (4 * k * r)
def eps_phys(rho_max_msun_kpc3, a0):
    rho = rho_max_msun_kpc3 * MSUN / KPC ** 3; return (8 * math.pi / 3 * G_SI * rho * C ** 2 / a0 ** 2) ** -0.5
def sech2(x):
    e = np.exp(-2 * np.abs(x)); return 4 * e / (1 + e) ** 2
say("=" * 92); say(f"FA1 / I6 Galileon determinant. MUTATE={MUT}. D {D_DUST}, rms line {RMS_LINE:.4f} dex, f_max {F_MAX:.4f}")

# ---------------- K0, K1
def law(g, a): return g * (0.5 + np.sqrt(0.25 + a / g))
gg = np.geomspace(1e-14, 1e-6, 200)
for f in FEET:
    d = float(np.max(np.abs(law(gg, A0[f]) * (1 + 0.0 * D_DUST) / law(gg, A0[f]) - 1))); check(f"K0 F=0 reproduces the law, {f}", d < 1e-12, f"{d:.1e}")
spt = float(gs.s_from_n(-0.5)); ex = -3 * math.sqrt(3) / (2 * (9 / 4) ** 1.5)
check("K1 uniform sphere s = 1", abs(float(gs.s_from_n(1.0)) - 1) < 1e-12, f"{float(gs.s_from_n(1.0)):.12f}")
check("K1 deep point mass s", abs(spt - ex) < 1e-9, f"{spt:.6f} vs {ex:.6f}")
eps_t = 1e-3; rr = np.geomspace(0.01, 50, 400); hstep = 1e-4
def dp_pl(x): return gs.dphi_sph(x, x ** 3 / (3 * (1 + x * x) ** 1.5), eps_t)
p1 = dp_pl(rr); p2 = (dp_pl(rr * math.exp(hstep)) - dp_pl(rr * math.exp(-hstep))) / (2 * hstep) / rr
lhs = eps_t * (p2 + 2 * p1 / rr) + 2 * (2 * p2 * p1 / rr + (p1 / rr) ** 2); Sx = (1 + rr * rr) ** -2.5
rel = float(np.max(np.abs(lhs - Sx) / np.maximum.reduce([Sx, np.abs(lhs), eps_t * np.abs(p2 + 2 * p1 / rr)])))
check("K1 spherical quadratic satisfies the static equation", rel < 1e-6, f"max rel {rel:.1e}")

# ---------------- X-COP rows, s_c per footing
from astropy.io import fits
D = os.path.join(REPO, "real_research", "data", "xcop"); XC = []
def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
for name in sorted(os.listdir(D)):
    p = os.path.join(D, name)
    if not (os.path.isdir(p) and os.path.exists(os.path.join(p, f"{name}_mstar.fits"))): continue
    with fits.open(os.path.join(p, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
    with fits.open(os.path.join(p, f"{name}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
    with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    for x in (.1, .2, .3, .5, .7):
        r = x * r5; ms = [li(ga["RADIUS"] * rg, ga["MGAS"], q) + li(st["RADIUS"], st["MSTAR"], q) for q in (r / 1.1, r, r * 1.1)]
        if np.all(np.isfinite(ms + [li(hm["RADIUS"], hm["M_FORW"], r)])): XC.append(dict(n=name, x=x, r_m=r * KPC, M=[m * MSUN for m in ms]))   # R500 header is in kpc
SC = {}; RES["xcop"] = dict(n=len(XC), footings={})
for f in FEET:
    s = []
    for c in XC:
        rq = np.array([c["r_m"] / 1.1, c["r_m"], c["r_m"] * 1.1]); dp = dpi_phys(rq, np.array(c["M"]), A0[f])
        n = (math.log(dp[2]) - math.log(dp[0])) / (2 * math.log(1.1)); s.append(float(gs.s_from_n(n)))
    s = np.array(s); SC[f] = float(np.percentile(s, 5))
    RES["xcop"]["footings"][f] = dict(s_c=SC[f], s_min=float(s.min()), s_median=float(np.median(s)), s_max=float(s.max()), frac_pos=float((s > 0).mean()))
    say(f"[{f}] X-COP {len(XC)} rows: s min {s.min():.4f}, s_c (5th pct) {SC[f]:.4f}, median {np.median(s):.4f}, max {s.max():.4f}; s > 0 in {(s > 0).mean():.2f}")

# ---------------- G6-SPH, SPARC spherical-equivalent
files = sorted(glob.glob(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod", "*_rotmod.dat")))
SP = {os.path.basename(fp).replace("_rotmod.dat", ""): np.loadtxt(fp, comments="#", ndmin=2) for fp in files}
for f in FEET:
    o = {}
    for Y in (0.5, 0.3, 0.7):
        ss = []
        for name, a in SP.items():
            R, Vg, Vd, Vb = a[:, 0], a[:, 3], a[:, 4], a[:, 5]; V2 = np.sign(Vg) * Vg ** 2 + Y * Vd ** 2 + 1.4 * Y * Vb ** 2
            gb = V2 * 1e6 / (R * KPC); ok = (V2 > 0) & (R > 0)
            if ok.sum() < 3: continue
            r_m = R[ok] * KPC; M = r_m * V2[ok] * 1e6 / G_SI; dp = dpi_phys(r_m, M, A0[f]); n = np.gradient(np.log(dp), np.log(r_m))
            sv = SIGN * gs.s_from_n(n); sel = gb[ok] < A0[f]; ss.append(sv[sel])
        ss = np.concatenate(ss); o[f"Y{Y}"] = dict(n=int(len(ss)), f_SP=float((ss >= SC[f]).mean()), s_median=float(np.median(ss)))
    fs = [o[k]["f_SP"] for k in ("Y0.5", "Y0.3", "Y0.7")]
    o["label"] = "SEPARATES" if all(v <= F_MAX for v in fs) else ("DOES NOT SEPARATE" if all(v > F_MAX for v in fs) else "UNDECIDED")
    RES.setdefault("G6-SPH", {})[f] = o
    say(f"[{f}] G6-SPH: " + "; ".join(f"Y {k[1:]}: n {o[k]['n']}, f_SP {o[k]['f_SP']:.3f}, median s {o[k]['s_median']:+.3f}" for k in ("Y0.5", "Y0.3", "Y0.7")) + f" -> {o['label']}")

# ---------------- axisymmetric solves
def alpha_for(L, N, dz):
    return brentq(lambda a: L * a / (N * math.sinh(a)) - dz, 1e-3, 30.0)
def run_solve(rho_fn, rho_max, L, N, alpha, eps, label):
    g = gs.Grid(N, L, alpha); fn = lambda R, z: rho_fn(R, z) / rho_max
    Rn, Zn = np.meshgrid(g.x, g.x, indexing="ij"); S = fn(Rn, Zn)[:N, :N]
    phi0, _ = gs.spherical_guess(g, fn, eps); t = time.time(); phi, h = gs.solve(g, S, eps, phi0)
    ok = h[-1] < 1e-9; say(f"    solve {label}: N {N}, L {L:.1f}, alpha {alpha:.2f}, eps {eps:.2e}: |res| {h[0]:.1e} -> {h[-1]:.1e} in {len(h) - 1} steps, {time.time() - t:.1f} s{'' if ok else '  NOT CONVERGED'}")
    return g, gs.interp_s(g, gs.selector(g, phi)), ok
# K2: spherical Plummer
gP, siP, okP = run_solve(lambda R, z: (1 + R * R + z * z) ** -2.5, 1.0, 40.0, 192, 4.0, 1e-3, "K2 Plummer")
worst = 0.0
for r in (0.3, 0.5, 1, 2, 3, 5):
    dp = lambda x: gs.dphi_sph(x, x ** 3 / (3 * (1 + x * x) ** 1.5), 1e-3); n = (math.log(dp(r * 1.001)) - math.log(dp(r / 1.001))) / (2 * math.log(1.001))
    for m in (0.1, 0.5, 0.9): worst = max(worst, abs(float(siP(np.array(r * math.sqrt(1 - m * m)), np.array(r * m)).item()) - float(gs.s_from_n(n))))
check("K2 axisymmetric solver on a spherical Plummer", okP and worst < 0.02, f"max |ds| {worst:.4f}")

# G6-CL: X-COP-like cluster
R500, RCORE, BETA, MGAS, MBCG, ABCG = 1300.0, 195.0, 0.7, 1e14, 1e12, 30.0
def gas_shape(r): return (1 + (r / RCORE) ** 2) ** (-1.5 * BETA) * np.exp(-(r / (2 * R500)) ** 4)
rq = np.linspace(0, R500, 20001); norm = MGAS / np.trapz(4 * math.pi * rq ** 2 * gas_shape(rq), rq)
def rho_cl(R, z):
    r = np.hypot(R, z); rs = np.sqrt(r * r + 1.0)
    return norm * gas_shape(r) + MBCG * ABCG / (2 * math.pi * rs * (rs + ABCG) ** 3)
rmax_cl = float(rho_cl(np.array(0.0), np.array(0.0))); RES["G6-CL"] = {}
for f in FEET:
    L = 20 * R500; N = 192; al = alpha_for(L, 96, 5.0); g, si, ok = run_solve(rho_cl, rmax_cl, L, N, al, eps_phys(rmax_cl, A0[f]), f"cluster {f}")
    vals = [float(si(np.array(x * R500 * math.sqrt(1 - m * m)), np.array(x * R500 * m)).item()) for x in (0.1, 0.2, 0.3, 0.5, 0.7) for m in (0.1, 0.5, 0.9)]
    lab = "ON" if (ok and min(vals) >= SC[f]) else "NOT ON"
    RES["G6-CL"][f] = dict(s_min=min(vals), s_max=max(vals), s_c=SC[f], label=lab, points={f"x{x}_mu{m}": round(v, 4) for (x, m), v in zip([(x, m) for x in (0.1, 0.2, 0.3, 0.5, 0.7) for m in (0.1, 0.5, 0.9)], vals)}); say(f"[{f}] G6-CL: s on 0.1-0.7 R500 at 3 angles: {min(vals):.3f}-{max(vals):.3f} vs s_c {SC[f]:.3f} -> {lab}")

# G6-DISC: six SPARC galaxies
T1 = {}
for ln in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = ln.split()
    if len(p) >= 18 and not ln.startswith(("Title", "Note", "Byte", "Authors", "Table")):
        try: T1[p[0]] = dict(L=float(p[7]) * 1e9, Rd=float(p[11]), MHI=float(p[13]) * 1e9, RHI=float(p[14]))
        except ValueError: pass
MODELS = ["DDO154", "NGC3741", "IC2574", "NGC2403", "NGC3198", "UGC00128"]
def model(name):
    t = T1[name]; Ms, Rd, z0 = 0.5 * t["L"], t["Rd"], 0.15 * t["Rd"]; Mg = 1.33 * t["MHI"]
    fq = lambda Rg: math.log(t["MHI"] / (2 * math.pi * Rg * Rg)) - t["RHI"] / Rg - math.log(1e6)
    Rg = brentq(fq, t["RHI"] / 2, 100 * t["RHI"]) if fq(t["RHI"] / 2) > 0 else t["RHI"] / 2; zg = 0.1 * Rg
    def rho(R, z): return Ms / (4 * math.pi * Rd ** 2 * z0) * np.exp(-R / Rd) * sech2(z / z0) + Mg / (4 * math.pi * Rg ** 2 * zg) * np.exp(-R / Rg) * sech2(z / zg)
    a = SP[name]; return dict(Ms=Ms, Rd=Rd, z0=z0, Mg=Mg, Rg=Rg, zg=zg, rho=rho, rho_max=float(rho(np.array(0.0), np.array(0.0))), R=a[:, 0], V2=np.sign(a[:, 3]) * a[:, 3] ** 2 + 0.5 * a[:, 4] ** 2 + 0.7 * a[:, 5] ** 2)
def grade_model(m, si, f, sc):
    gb = m["V2"] * 1e6 / (m["R"] * KPC); Rs = m["R"][(gb > 0) & (gb < A0[f])]
    if len(Rs) == 0: return dict(n=0, label="NO LOW-g POINTS")
    W = np.array([gs.shell_W(si, x, sc, sign=SIGN) for x in Rs]); We = np.array([gs.W_enc(si, x, sc, sign=SIGN) for x in Rs])
    dl = np.log10(1 + D_DUST * We); rms = float(np.sqrt(np.mean(dl ** 2)))
    mid = np.array([SIGN * float(si(np.array(x), np.array(0.0)).item()) for x in Rs])
    return dict(n=int(len(Rs)), R=[round(float(x), 3) for x in Rs], W=[round(float(x), 4) for x in W], W_enc=[round(float(x), 4) for x in We], s_mid=[round(float(x), 4) for x in mid], rms_delta=rms, label="ON" if rms > RMS_LINE else "OFF")
RES["G6-DISC"] = {f: {} for f in FEET}; LAD = {}
for name in MODELS:
    m = model(name); Lb = max(40 * max(m["Rd"], m["Rg"]), 4 * float(m["R"].max())); dz = min(m["z0"], m["zg"]) / 3
    say(f"  model {name}: M* {m['Ms']:.2e} R_d {m['Rd']:.2f} | M_gas {m['Mg']:.2e} R_g {m['Rg']:.2f} kpc | last R {m['R'].max():.1f} | box {Lb:.0f} kpc")
    al = alpha_for(Lb, 96, dz)
    for f in FEET:
        e0 = eps_phys(m["rho_max"], A0[f]); Ns = (192,) if MUT else (48, 96, 192); gr = {}
        for N in Ns:
            g, si, ok = run_solve(m["rho"], m["rho_max"], Lb, N, al, e0, f"{name} {f}"); gr[N] = grade_model(m, si, f, SC[f]); gr[N]["converged"] = ok
        o = gr[192]; RES["G6-DISC"][f][name] = o
        say(f"  [{f}] {name} N192: n {o['n']} low-g radii, rms delta {o['rms_delta']:.4f} -> {o['label']}; W_enc {min(o['W_enc']):.3f}-{max(o['W_enc']):.3f}; W {min(o['W']):.3f}-{max(o['W']):.3f}; midplane s {min(o['s_mid']):+.3f} to {max(o['s_mid']):+.3f}")
        if not MUT:
            d96 = float(np.max(np.abs(np.array(gr[96]["W_enc"]) - np.array(gr[192]["W_enc"])))); d48 = float(np.max(np.abs(np.array(gr[48]["W_enc"]) - np.array(gr[192]["W_enc"]))))
            LAD[f"{name}|{f}"] = dict(dW_96_192=d96, dW_48_192=d48, same_label=gr[96]["label"] == gr[192]["label"], rms=[gr[N]["rms_delta"] for N in Ns], conv=all(gr[N]["converged"] for N in Ns))
            say(f"     ladder: rms delta N48/96/192 {gr[48]['rms_delta']:.4f}/{gr[96]['rms_delta']:.4f}/{gr[192]['rms_delta']:.4f}; max dW_enc 96-192 {d96:.4f}, 48-192 {d48:.4f}")
            if f == "canonical":
                g, si, ok = run_solve(m["rho"], m["rho_max"], 2 * Lb, 96, alpha_for(2 * Lb, 96, dz), e0, f"{name} box x2"); bx = grade_model(m, si, f, SC[f])
                g, si, ok2 = run_solve(m["rho"], m["rho_max"], Lb, 96, al, 10 * e0, f"{name} eps x10"); ex10 = grade_model(m, si, f, SC[f])
                LAD[f"{name}|{f}"].update(dW_box=float(np.max(np.abs(np.array(bx["W_enc"]) - np.array(gr[96]["W_enc"])))), dW_eps=float(np.max(np.abs(np.array(ex10["W_enc"]) - np.array(gr[96]["W_enc"])))), conv_var=ok and ok2)
                say(f"     box x2: max dW_enc {LAD[f'{name}|{f}']['dW_box']:.4f}; eps x10: {LAD[f'{name}|{f}']['dW_eps']:.4f}")
for f in FEET:
    on = [k for k, v in RES["G6-DISC"][f].items() if v["label"] == "ON"]
    RES["G6-DISC"][f]["label"] = "SWITCHES OFF" if not on else "DOES NOT SWITCH OFF"; RES["G6-DISC"][f]["on_models"] = on
    say(f"[{f}] G6-DISC: {len(on)} of 6 ON {on} -> {RES['G6-DISC'][f]['label']}")
if not MUT:
    RES["ladder"] = LAD
    check("Ladder N96 vs N192 (dW_enc <= 0.03, same ON/OFF, converged)", all(v["dW_96_192"] <= 0.03 and v["same_label"] and v["conv"] for v in LAD.values()), f"max {max(v['dW_96_192'] for v in LAD.values()):.4f}")
    check("Ladder box x2 and eps x10 (dW_enc <= 0.03)", all(v["dW_box"] <= 0.03 and v["dW_eps"] <= 0.03 and v["conv_var"] for k, v in LAD.items() if k.endswith("canonical")),
          f"box max {max(v['dW_box'] for k, v in LAD.items() if k.endswith('canonical')):.4f}, eps max {max(v['dW_eps'] for k, v in LAD.items() if k.endswith('canonical')):.4f}")

# ---------------- G6-Q2 (order of magnitude)
AU, GMS = 149597870700.0, 1.32712440018e20; rho_loc = 0.1 * MSUN / (3.0857e16) ** 3; Q2 = {}
for f in FEET:
    a0 = A0[f]; o = {}
    for pl, rau, bound in (("Saturn", 9.5826, 7e-15), ("Mars", 1.5237, 1.4e-15), ("Earth", 1.0, 8.7e-15)):
        r = rau * AU; rr3 = np.array([r / 1.01, r, r * 1.01]); M = GMS / G_SI + 4 * math.pi / 3 * rho_loc * rr3 ** 3; dp = dpi_phys(rr3, M, a0)
        n = (math.log(dp[2]) - math.log(dp[0])) / (2 * math.log(1.01)); o[pl] = dict(s=float(gs.s_from_n(n)), a_pi=float(dp[1] / 2), bound=bound, ratio=float(dp[1] / 2 / bound))
    R0 = 8.2 * KPC; Mmw = (220e3) ** 2 * R0 / G_SI; dmw = dpi_phys(np.array([R0]), np.array([Mmw]), a0)[0]; tid = 0.5 * dmw / R0
    o["MW_tidal"] = dict(pi_prime=float(dmw), tidal=float(tid), hees=9e-27, ratio=float(tid / 9e-27))
    okQ = o["Saturn"]["s"] < SC[f] and o["Saturn"]["ratio"] < 0.1 and o["MW_tidal"]["ratio"] < 0.1
    o["label"] = "PASS" if okQ else "FAIL"; Q2[f] = o
    say(f"[{f}] G6-Q2: s at Saturn {o['Saturn']['s']:+.4f} (s_c {SC[f]:.3f}); pi force / bound: Saturn {o['Saturn']['ratio']:.2f}, Mars {o['Mars']['ratio']:.2f}, Earth {o['Earth']['ratio']:.2f}; MW pi tidal {tid:.1e} s^-2 / Hees {o['MW_tidal']['ratio']:.1e} -> {o['label']}")
    cpl = (0.1 / o["Saturn"]["ratio"]) ** (2 / 3); o["coupling_for_saturn_0.1"] = float(cpl)
    say(f"     reported: the pi force scales as beta^1.5 with the matter coupling beta (frozen beta = 1); Saturn at 0.1 needs beta <= {cpl:.2f}; s is beta-independent in the deep regime")
RES["G6-Q2"] = Q2
RES["G6-GW"] = dict(label="PASS (CONDITIONAL: F flat near s = 1)", note="L2 + L3 keep c_T = c; the selector term shifts the tensor kinetic coefficient by O(Omega_d F'(1)); GW170817 -3e-15 < dc/c < 7e-16 (PROVISIONAL) needs F'(1) <~ 1e-15 / Omega_d; a step F has F'(1) = 0. L4/L5 omitted (O(1) alpha_T on galileon backgrounds).")
RES["action"] = "writable; F depends on second derivatives of pi, so it is healthy (no Ostrogradsky mode) only for F flat on the dust's support"
RES["G6-BUL"] = "NOT COMPUTED"; RES["keys"] = "NOT COMPUTED"

# ---------------- labels
RES["checks"] = CHECKS; allok = all(CHECKS.values()); lab = {}
for f in FEET:
    dsc = RES["G6-DISC"][f]["label"]
    lab[f] = ("I6 KILLED AT THE SPARC NULL" if dsc == "DOES NOT SWITCH OFF" else
              "I6 ALIVE AT GATE 1" if (dsc == "SWITCHES OFF" and RES["G6-CL"][f]["label"] == "ON" and Q2[f]["label"] == "PASS") else
              f"UNDECIDED (DISC {dsc}, CL {RES['G6-CL'][f]['label']}, Q2 {Q2[f]['label']})")
lane = lab["canonical"] if lab["canonical"] == lab["alt"] else "FOOTING-SPLIT: " + " | ".join(lab[f] for f in FEET)
if not allok: lane = "NO CLEAN LABEL (a check failed): " + lane
RES["lane_label"] = lane; say(f"LANE: {lane}" + ("  [MUTATE twin]" if MUT else ""))
json.dump(RES, open(os.path.join(HERE, f"i6_results{TAG}.json"), "w"), indent=1, sort_keys=True)
OUT.close()
