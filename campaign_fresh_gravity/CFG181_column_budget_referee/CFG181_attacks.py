#!/usr/bin/env python3
# CFG181 attacks A-G (frozen grids in CFG181_FROZEN_CRITERIA.md section 6). Exit 0. No repo import.
import os, sys, json, math, itertools
sys.dont_write_bytecode = True
import numpy as np, sympy as sp
from CFG181_common import *
HERE = os.path.dirname(os.path.abspath(__file__))
lines = []; res = {}
def P(s=""): print(s); lines.append(s)
H, OL = 0.674, 0.685; T0 = 13.79 * GYR; LO, HI = 0.1, 1.0
inl = lambda R: LO <= R <= HI
rL = rho_L(H, OL); base_sig = a0 = A0_A
R0 = Sigma_P2(A0_A) / swept(H, OL, T0)

# ================= A
P("=== A: genuine test or restatement ===")
a_lo, a_hi = LO * 2 * math.pi * G * rL * C * T0, HI * 2 * math.pi * G * rL * C * T0
P(f"Q1 accepts a0 in [{a_lo:.3e}, {a_hi:.3e}] m/s^2 ({math.log10(a_hi/a_lo):.2f} dex wide); c*H0 = {C*H0_si(H):.3e}; a0(A)/(cH0) = {A0_A/(C*H0_si(H)):.3f}")
lit = [0.8e-10, 1.0e-10, 1.13e-10, 1.2e-10, 1.4e-10]
litR = {a: Sigma_P2(a) / swept(H, OL, T0) for a in lit}
kap = [0.35, 0.465, 0.5, 0.55, 0.72]
kapR = {k: Sigma_P2(k * C * math.sqrt(G * rL)) / swept(H, OL, T0) for k in kap}
P("literature-scale a0: " + ", ".join(f"{a:.2e}:R={v:.3f}({'pass' if inl(v) else 'FAIL'})" for a, v in litR.items()))
P("kappa grid: " + ", ".join(f"{k}:R={v:.3f}({'pass' if inl(v) else 'FAIL'})" for k, v in kapR.items()))
rng = np.linspace(-13, -7, 60001); frac = np.mean([inl(Sigma_P2(10**l) / swept(H, OL, T0)) for l in rng[::10]])
P(f"null-world count (informational): a0 log-uniform 1e-13..1e-7 -> fraction passing Q1 = {frac:.3f}")
allpass = all(inl(v) for v in list(litR.values()) + list(kapR.values()))
A_verdict = "RESTATEMENT" if allpass else "GENUINE"
P(f"A verdict (Q1): {A_verdict}: every literature a0 and kappa value passes = {allpass}; no galaxy-scale quantity enters R (sympy: mass-free, see main).")
P("Q2: a requirement (deposit shape), not a test. Q3: the only falsifiable statement; a rival to (not a consequence of) the framework's flat-a0 law (noted, not scored). Q4: see F.")
res["A"] = dict(window=[a_lo, a_hi], dex=math.log10(a_hi / a_lo), lit=litR, kappa=kapR, null_frac=frac, verdict=A_verdict)

# ================= B
P(""); P("=== B: declared choices, one-at-a-time and joint grid ===")
colfac = {"CFG174 M_c/pi r^2": 1.0, "shell M_c/4pi r^2": 0.25, "central rho_c r": 0.5}
for Z in (1, 3, 10, 100): colfac[f"projected Z/R={Z}"] = math.asinh(Z)
def Rcell(colf=1.0, u=C, t=T0, kern=1.0, a0=A0_A, h=H, ol=OL):
    return colf * kern * Sigma_P2(a0) / swept(h, ol, t, u)
flips = {}
def axis(name, cells):
    out = {}
    for k, v in cells.items(): out[k] = (v, inl(v))
    P(f"axis {name}: " + "; ".join(f"{k}: R={v:.4g}{'' if ok else ' FLIP'}" for k, (v, ok) in out.items()))
    flips[name] = [k for k, (v, ok) in out.items() if not ok]; res.setdefault("B", {})[name] = {k: v for k, (v, ok) in out.items()}
axis("column", {k: Rcell(colf=f) for k, f in colfac.items()})
axis("speed", {f"u/c={u}": Rcell(u=u * C) for u in (1, 0.3, 0.1, 0.01)} | {"600 km/s": Rcell(u=600e3), "370 km/s": Rcell(u=370e3)})
Hh, Oo = H, OL
tz = lambda z: t_of_z(Hh, Oo, z)
axis("duration", {"t0": Rcell(t=T0), "t0/2": Rcell(t=T0 / 2), "t(z=1)": Rcell(t=tz(1)), "t(z=2)": Rcell(t=tz(2)), "1 Gyr": Rcell(t=GYR)})
axis("kernel", {"CFG44 P2": Rcell(), "simple 1/2+sqrt(1/4+1/y)": Rcell(kern=2.0)})
axis("a0 footing", {"A 9.36e-11": Rcell(a0=A0_A), "B 1.13e-10": Rcell(a0=A0_B)})
cosmos = [(0.674, 0.685), (0.6766, 0.6889), (0.70, 0.70), (0.73, 0.70)]
axis("cosmology (own flat age)", {f"H0={h*100:.2f},OL={o}": Rcell(h=h, ol=o, t=age_flat(h, o)) for h, o in cosmos})
one_at_a_time_flips = {k: v for k, v in flips.items() if v}
P(f"one-at-a-time axes with at least one flipping cell: {list(one_at_a_time_flips)}")
# joint set: 3 columns x 2 kernels x 2 footings x 4 cosmologies (48 cells at u=c, own age)
jc = {"CFG174 M_c/pi r^2": 1.0, "central rho_c r": 0.5, "projected Z/R=3": math.asinh(3)}
cells = [(cn, kn, fn, cs) for cn in jc for kn in (1.0, 2.0) for fn in (A0_A, A0_B) for cs in cosmos]
Rj = [Rcell(colf=jc[cn], kern=kn, a0=fn, h=cs[0], ol=cs[1], t=age_flat(*cs)) for cn, kn, fn, cs in cells]
npass = sum(inl(v) for v in Rj)
P(f"joint plausible set: {len(Rj)} cells, R range {min(Rj):.3f}-{max(Rj):.3f}, passing {npass}/{len(Rj)}")
P(f"one-sided line R<=1 instead of two-sided: shell column R={Rcell(colf=.25):.3f} would PASS; a0 x 0.1 R={Rcell(a0=0.1*A0_A):.3f} would PASS; the two-sided lower bound 0.1 is what makes them fail")
B_verdict = "DEFINITION-DEPENDENT" if one_at_a_time_flips else "ROBUST"
P(f"B verdict: {B_verdict}")
res["B"]["joint"] = dict(n=len(Rj), passing=int(npass), Rmin=min(Rj), Rmax=max(Rj)); res["B"]["verdict"] = B_verdict; res["B"]["flip_axes"] = one_at_a_time_flips

# ================= C
P(""); P("=== C: scale-free or circular ===")
k_, H0s, t_, OLs, G_, rho_, c_, a0_ = sp.symbols("kappa H0 t Omega_L G rho c a0", positive=True)
rho_sym = 3 * H0s**2 * OLs / (8 * sp.pi * G_)
Rk = sp.simplify((k_ * c_ * sp.sqrt(G_ * rho_sym) / (2 * sp.pi * G_)) / (rho_sym * c_ * t_))
Rclosed = k_ / (2 * sp.pi) / (H0s * t_) / sp.sqrt(3 * OLs / (8 * sp.pi))
sym_eq = sp.simplify(Rk - Rclosed) == 0
P(f"sympy: R = kappa/(2 pi) * 1/(H0 t) * 1/sqrt(3 Omega_L/8 pi) -> identity {sym_eq}; contains no mass or radius symbol")
Hs = H0_si(H); cosmo_num = 1 / (2 * math.pi * Hs * T0 * math.sqrt(3 * OL / (8 * math.pi)))
P(f"numerical: kappa=0.5 -> R = {0.5*cosmo_num:.4f}; cosmology-only factor (per unit kappa) = {cosmo_num:.4f}; H0*t0 = {Hs*T0:.4f}")
e = 1e-6; dl = (math.log(Sigma_P2(A0_A * (1 + e)) / swept(H, OL, T0)) - math.log(Sigma_P2(A0_A * (1 - e)) / swept(H, OL, T0))) / (math.log(1 + e) - math.log(1 - e))
P(f"d ln R / d ln a0 = {dl:.9f}")
tw = [0.1, 1.0, 10.0]; Rt = {f: Rcell(t=f * T0) for f in tw}
tl, th = T0 * R0 / HI / GYR, T0 * R0 / LO / GYR
P("R(t) at fixed a0: " + ", ".join(f"t0*{f}: {v:.3f}" for f, v in Rt.items()) + f"; the line holds for t in [{tl:.2f}, {th:.1f}] Gyr")
C_verdict = "SCALE-FREE (mass-independent) and NOT a0-independent"
P(f"C verdict: {C_verdict}")
res["C"] = dict(sym_identity=bool(sym_eq), dlnR_dlna0=dl, cosmo_factor=cosmo_num, t_window_Gyr=[tl, th], verdict=C_verdict)

# ================= D
P(""); P("=== D: kernel dependence of the column (point mass; unit a0/(2 pi G)) ===")
nu_mono = build_nu_mono()
kern = {"CFG44 P2": nu_p2, "simple": nu_simple, "McGaugh RAR": nu_rar, "nu_mono (shared definition)": nu_mono}
xs = np.geomspace(1e-3, 1e2, 4001); ys = 1 / xs**2
Dres = {}
for n, nu in kern.items():
    c = col_units(nu, ys); i = int(np.argmax(c))
    c1 = {x: float(col_units(nu, np.array([1 / x**2]))[0]) for x in (1e-3, 1e-2, 0.1, 1.0)}
    Dres[n] = dict(sup=float(c[i]), x_at_sup=float(xs[i]), at=c1, R_sup=float(c[i] * R0), R_x0p1=float(c1[0.1] * R0))
    plateau = "plateau" if (c1[1e-3] > 0.05 and abs(c1[1e-3] - c1[1e-2]) / c1[1e-2] < 0.01) else ("NO plateau (column -> 0)" if c1[1e-3] < 0.05 else "NO plateau (keeps growing)")
    P(f"{n:28s} sup column {c[i]:8.4f} at x={xs[i]:.3g}; at x=1e-3,1e-2,0.1,1: " + ", ".join(f"{v:.4g}" for v in c1.values()) + f" -> {plateau}; R at sup {c[i]*R0:.3f}, at x=0.1 {c1[0.1]*R0:.4f}")
res["D"] = Dres
D_verdict = "P2-specific constant: RAR column -> 0 at small x (no plateau)" if Dres["McGaugh RAR"]["at"][1e-3] < 0.01 else "RAR plateau"
mm = Dres["nu_mono (shared definition)"]["at"]; mono_plateau = abs(mm[1e-3] - mm[1e-2]) < 0.01 * mm[1e-2]
P(f"D verdict: {D_verdict}; nu_mono plateau at small x: {mono_plateau} (frozen expectation was that BOTH RAR and nu_mono columns vanish at small x: RAR does; nu_mono does NOT, its monotone repair adds a slowly (log) growing extra acceleration, so its column grows toward small x: WRONG expectation, kept)")
res["D_verdict"] = D_verdict

# ================= E
P(""); P("=== E: Q3 assumptions ===")
def dexz(h, om, z, zon=None, Or=0.0):
    t0_ = age_flat(h, 1 - om - Or, Or); tz_ = t_of_z(h, 1 - om, z) if Or == 0 else None
    if zon is None: return math.log10(tz_ / t0_)
    ton = t_of_z(h, 1 - om, zon); return math.log10((tz_ - ton) / (t0_ - ton))
cos3 = [(0.6766, 0.3111), (0.674, 0.315), (0.70, 0.30), (0.73, 0.30)]
Eres = {}; alld = []
for zon in (None, 20, 10, 5):
    for h, om in cos3:
        row = [dexz(h, om, z, zon) for z in (0.85, 1.5, 2.5)]; Eres[f"zon={zon},H0={h*100:.2f},Om={om}"] = row; alld += row
    P(f"z_on={zon}: dex at (0.85,1.5,2.5) for the 4 cosmologies: " + " | ".join(f"({', '.join(f'{v:+.3f}' for v in Eres[f'zon={zon},H0={h*100:.2f},Om={om}'])})" for h, om in cos3))
Or = 9.2e-5
rad = [(math.log10(t_of_z(0.6766, 0.6889, z) / age_flat(0.6766, 0.6889)), None) for z in (1.5,)]
# radiation: age with Or, and t(z) by integrating from a=0 to 1/(1+z)
from scipy.integrate import quad
def age_rad(h, om, a1):
    Or_ = 9.2e-5; ol = 1 - om - Or_
    return quad(lambda a: 1 / (H0_si(h) * math.sqrt(om / a + Or_ / a**2 + ol * a**2)), 0, a1, limit=200)[0]
rdex = {z: math.log10(age_rad(0.6766, 0.3111, 1 / (1 + z)) / age_rad(0.6766, 0.3111, 1.0)) for z in (0.85, 1.5, 2.5)}
P(f"radiation included (Omega_r=9.2e-5, Om=0.3111 with flat closure): t0 = {age_rad(0.6766,0.3111,1.0)/GYR:.3f} Gyr; dex " + ", ".join(f"z={z}: {v:+.3f}" for z, v in rdex.items()))
sign_robust = all(v < 0 for v in alld) and all(v < 0 for v in rdex.values())
z15 = [Eres[k][1] for k in Eres]; spread = max(z15) - min(z15)
P(f"sign robust (falls with z in every cell): {sign_robust}; z=1.5 amplitude range {min(z15):+.3f} to {max(z15):+.3f} (spread {spread:.3f} dex; frozen threshold 0.1 -> {'assumption-dependent amplitude' if spread>0.1 else 'amplitude stable'})")
P("consistency with Q1: the present-day match a0(t0) fixes u/c = R independent of z, so Q3 does not depend on u.")
res["E"] = dict(grid=Eres, radiation=rdex, sign_robust=bool(sign_robust), spread_z15=spread)

# ================= F
P(""); P("=== F: Q4 borders and scaling ===")
mass = [14, 14.5, 15]; refs = {}
Om = 1 - OL
def ratio(a0v, delta, rho_ref, fb, ref):
    out = []
    for lm in mass:
        M = 10**lm; R = r500(M, H, delta, rho_ref); col = a0v / (2 * math.pi * G) * math.pi * R**2 / MSUN
        if ref == "need": den = (1 - fb) * M
        else:
            Mb = fb * M; x = R * math.sqrt(A0_A / (G * Mb * MSUN)); den = Mb * (math.sqrt(1 + x**2) - 1)
        out.append(col / den)
    return out
defs = {"500 rho_crit": (500, rho_crit(H)), "200 rho_crit": (200, rho_crit(H)), "500 rho_mean": (500, Om * rho_crit(H))}
Fres = {}; nflip = 0; ncell = 0
for ref in ("need (1-fb) M500", "law phantom (P2, M_b=fb M500)"):
    for dn, (dl_, rr) in defs.items():
        for fb in (0.10, 0.12, 0.15, 0.17):
            for fn, av in (("A", A0_A), ("B", A0_B)):
                r_ = ratio(av, dl_, rr, fb, "need" if ref.startswith("need") else "law"); ok = all(0.5 <= v <= 2 for v in r_)
                sl = (math.log10(r_[2]) - math.log10(r_[0])) / 1.0
                Fres[f"{ref}|{dn}|fb={fb}|{fn}"] = dict(r=r_, pass_line=ok, slope=sl)
                if ref.startswith("need"): ncell += 1; nflip += ok
P("baseline (need, 500 rho_crit, fb 0.15, A): " + ", ".join(f"{v:.3f}" for v in Fres["need (1-fb) M500|500 rho_crit|fb=0.15|A"]["r"]) + f" pass_line {Fres['need (1-fb) M500|500 rho_crit|fb=0.15|A']['pass_line']}")
P(f"reference 'need': {nflip}/{ncell} cells pass the factor-2 line at all three masses (baseline cell fails)")
for ref in ("need (1-fb) M500", "law phantom (P2, M_b=fb M500)"):
    sls = [v["slope"] for k, v in Fres.items() if k.startswith(ref)]
    P(f"{ref}: exponent d log(ratio)/d logM500 over cells: {min(sls):.3f} to {max(sls):.3f}")
lawb = Fres["law phantom (P2, M_b=fb M500)|500 rho_crit|fb=0.15|A"]
P(f"law-phantom reference, baseline: ratio {', '.join(f'{v:.2f}' for v in lawb['r'])}; law's own phantom at R500 vs the ΛCDM need: " + ", ".join(f"{lm}: {(0.15*10**lm*(math.sqrt(1+(r500(10**lm,H)*math.sqrt(A0_A/(G*0.15*10**lm*MSUN)))**2)-1))/(0.85*10**lm):.2f}" for lm in mass))
needs_flip = [k for k, v in Fres.items() if k.startswith("need") and v["pass_line"]]
sl_need = [v["slope"] for k, v in Fres.items() if k.startswith("need")]
F_scaling = all(abs(s + 1 / 3) <= 0.02 for s in sl_need)
F_verdict = ("FAIL label FRAGILE" if needs_flip else "FAIL label stable") + "; M^(2/3) scaling " + ("CONFIRMED" if F_scaling else "NOT confirmed")
P(f"F verdict: {F_verdict} ({len(needs_flip)} of {ncell} 'need' cells flip the baseline FAIL, e.g. {needs_flip[:3]})")
res["F"] = dict(cells=Fres, verdict=F_verdict, n_flip=len(needs_flip), n_cells=ncell)

# ================= G
P(""); P("=== G: Q2 label ===")
def f_an(x): return (math.sqrt(1 + x**2) - 1) / (x**2 / 2)
tf = [(0.1, 1.00), (1, 0.83), (10, 0.18), (30, 0.064)]
fS = {x: f_an(x) for x, _ in tf}; fSw = {x: R0 * f_an(x) for x, _ in tf}
P("README numbers (targets read): " + ", ".join(f"x={x}: {v}" for x, v in tf))
P("f normalised to Sigma_M: " + ", ".join(f"{x}: {fS[x]:.4f}" for x in fS) + "; fraction of the swept column R*f: " + ", ".join(f"{x}: {fSw[x]:.4f}" for x in fSw))
m1 = all(abs(fS[x] - v) <= 0.005 for x, v in tf); m2 = all(abs(fSw[x] - v) <= 0.005 for x, v in tf)
P(f"README numbers match Sigma_M-normalised f: {m1}; match fraction of swept column: {m2}")
P(f"local slope -> -1 at x = 30,100,1000: " + ", ".join(f"{(math.log(f_an(x*1.001))-math.log(f_an(x/1.001)))/(2*math.log(1.001)):.3f}" for x in (30, 100, 1000)))
G_verdict = "LABEL DISCREPANCY (README wording 'fraction of the swept column'; numbers are Sigma_M-normalised)" if m1 and not m2 else "no label discrepancy"
P(f"G verdict: {G_verdict}"); res["G"] = dict(f_Sigma=fS, f_swept=fSw, verdict=G_verdict)

open(f"{HERE}/CFG181_attacks.out", "w").write("\n".join(lines) + "\n")
json.dump(res, open(f"{HERE}/CFG181_attacks_results.json", "w"), indent=1, default=float)
