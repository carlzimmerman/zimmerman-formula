#!/usr/bin/env python3
"""Recompute the numbers in Argon's reply of 10-31 that can be checked here. kappa = 1/2 FITTED; not theory closed."""
import importlib.util, json, math, os, sys
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("Argon's reply of 10-31, recomputed; kappa = 1/2 FITTED; footings never pooled; not theory closed")
Om, h, wb = 0.2976016, 0.6856427, 0.0223081; Ob = wb / h ** 2; RN = (Om - Ob) / Ob; fc = RN / (1 + RN)
OmZ = lambda z: Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + 1 - Om); D18 = 18 * math.pi ** 2
P(f"A1 Delta_c(0) = 18 pi^2 Omega_m: {D18 * Om:.3f} (Argon 52.870). Omega_m(z_f 0.562) {OmZ(0.562):.4f} (Argon 0.770); Delta_c(z_f) {D18 * OmZ(0.562):.1f} (Argon 136.8)")
mu = lambda y: math.log(1 + y) - y / (1 + y); c = 5.72
from scipy.optimize import brentq
y = brentq(lambda y: mu(c * y) / mu(c) - (D18 * Om / 200) * y ** 3, 1.01, 4); P(f"A2 NFW c 5.72: R_52.87c/R_200c {y:.3f} (Argon 1.79); M ratio {mu(c * y) / mu(c):.3f} (Argon 1.348); S ratio at slope 0.228: {(mu(c * y) / mu(c)) ** 0.228:.3f}; MA1's own run: S/S_FC1 0.913 / 0.857 = {0.913 / 0.857:.3f}")
# native sigma(M), D(z), z_f
_s = importlib.util.spec_from_file_location("x48_zoom", os.path.join(REB, "X48_native_cf_zoom", "x48_zoom.py")); X = importlib.util.module_from_spec(_s); _s.loader.exec_module(X); C = X.cosmology()
sig = {l: float(C["sig"](10.0 ** l)[0]) for l in (10, 11, 12, 13, 14, 15)}; P("Q3a native sigma(M) at 1e12, 1e13, 1e14: " + ", ".join(f"{sig[l]:.3f}" for l in (12, 13, 14)) + " (Argon 2.05, 1.42, 0.94)")
D = lambda z: float(np.interp(z, C["ZG"], C["DG"])); P(f"Q3b 1/D(0.223) {1 / D(0.223):.3f} (Argon 1.125); 1/D(0.5) {1 / D(0.5):.3f}")
eta = {12: 25.937, 13: 17.666, 14: 16.914}; s13 = math.log(eta[14] / eta[13]) / math.log(sig[13] / sig[14]); s12 = math.log(eta[13] / eta[12]) / math.log(sig[12] / sig[13])
P(f"Q3c d ln eta / d ln nu: 1e13-1e14 {s13:.3f} (Argon about -0.12); 1e12-1e13 {s12:.3f}. Read at 1e13-1e14: eta at z_obs 0.223 x{(1 / D(0.223)) ** s13:.4f}, at 0.5 x{(1 / D(0.5)) ** s13:.4f} (Argon -1.5 %, -3.2 %). Read at 1e12-1e13: x{(1 / D(0.223)) ** s12:.4f}")
def zf(M, zo):
    lM = np.linspace(7, 16.5, 191); s2 = np.array([float(C["sig"](10 ** l)[0]) ** 2 for l in lM]); S = math.sqrt(float(np.interp(math.log10(M / 2), lM, s2)) - float(np.interp(math.log10(M), lM, s2)))
    return float(np.interp(-1.686 / (1.686 / D(zo) + 0.974 * S), -C["DG"], C["ZG"]))
for M in (2e14,): a, b = zf(M, 0.0), zf(M, 0.223); P(f"Q3d M {M:.0e}: z_f {a:.3f} at z_obs 0, {b:.3f} at 0.223; (1+z_f) ratio {(1 + b) / (1 + a):.3f} (Argon about 1.18); squared {((1 + b) / (1 + a)) ** 2:.3f} (lane's median S ratio 1.26)")
# ET ratios
N0, E1, E2 = (47, 69, 94), (69, 103, 143), (70, 108, 158); P("Q6a need/N0, ET1: " + ", ".join(f"{a / b:.2f}" for a, b in zip(E1, N0)) + "; ET2: " + ", ".join(f"{a / b:.2f}" for a, b in zip(E2, N0)) + " (Argon: exactly 1.50 at every bin against ET2's numbers). N1 72, 91, 112 gives ET2/N1 " + ", ".join(f"{a / b:.2f}" for a, b in zip(E2, (72, 91, 112))))
# cusp bound: the S in the rule is the smooth core's, not the NFW's rho_s r_s
X81P = os.path.join(REB, "X81_core_convergence", "x80_core_convergence.py"); src = open(X81P).read(); src = src[:src.index("# K1: exact smooth core")]; NS = dict(__file__=X81P, __name__="x81_prefix"); a0 = sys.argv; sys.argv = [X81P]; exec(compile(src, X81P, "exec"), NS); sys.argv = a0
ef, af, Mn = NS["eta_of"], NS["a_fit_profile"], NS["M_nfw"]; rows = []
for cc in (6.0, 7.75, 10.0, 15.0, 20.0):
    e = float(ef(af(Mn(cc), 0.001))); rs = cc * cc / (3 * mu(cc)); g = 2 * math.pi * rs / e / 1.599; rows.append((cc, e, rs, rs / e, g))
P("Q7a NFW rho_s r_s against the smooth-core S it fits, both over Delta rho r_f: " + "; ".join(f"c {r[0]:g}: eta {r[1]:.2f}, c^2/(3 m(c)) {r[2]:.2f}, ratio {r[3]:.3f}, ceiling gain x{r[4]:.2f} (+{math.log10(r[4]):.3f} dex)" for r in rows))
g = rows[3][4]; P(f"Q7b Argon's gain assumed the same S: 2 pi / 1.599 = {2 * math.pi / 1.599:.3f} (+{math.log10(2 * math.pi / 1.599):.3f} dex). At equal fit, c 15: +{math.log10(g):.3f} dex, so Draco on N1 +0.49 goes to {0.49 - math.log10(g):+.3f} dex, not -0.104; J0946 R 31 goes to {31 / g:.1f}, not 7.9")
# HSB/LSB example
Mh, Sg = 10 ** 10.73, 98.0; rc = 2.775e11 * h * h / 1e18; R2 = (3 * Mh / (4 * math.pi * 200 * rc)) ** (1 / 3); BS = lambda x: 4 * (math.asinh(x) - x / math.sqrt(1 + x * x)); r0 = brentq(lambda r: math.pi * Sg * r * r * BS(R2 / r) - Mh, 10, R2 / 2)
P(f"Q6b M200 10^10.73, S 98: R200 {R2 / 1e3:.1f} kpc, r0 {r0 / 1e3:.2f} kpc (Argon 5.8)")
P("Q6c -0.110 dex is in acceleration: -22 % in g, -11.9 % in V (Argon -22 % in V)")
# X-COP: baryon fraction inside R200 from X-COP's own measurements
ET = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json"))); fb = 1 / (1 + RN); rows = []
for n in sorted(ET):
    p = os.path.join(REPO, "real_research", "data", "xcop", n); gf = os.path.join(p, f"{n}_fgas_profile.fits"); sf = os.path.join(p, f"{n}_mstar.fits")
    if not os.path.exists(gf): continue
    with fits.open(gf) as hh: g_ = hh[1].data.copy(); rg = hh[1].header["R500"]
    r = g_["RADIUS"] * rg; R2_ = ET[n]["R200"] * 1e3
    if R2_ > r[-1]: rows.append((n, None, None, r[-1] / R2_)); continue
    Mg = 10 ** np.interp(np.log10(R2_), np.log10(r), np.log10(g_["MGAS"])); fg = Mg / (ET[n]["M200"] * 1e14); rows.append((n, fg, fg / fb, 1.0))
ok = [q for q in rows if q[1] is not None]; P(f"B1 X-COP measured gas inside R200 / hydrostatic M200 (stars not included), cosmic fraction here {fb:.4f}: " + ", ".join(f"{q[0]} {q[1]:.3f}" for q in ok) + f"; median Y_gas {np.median([q[2] for q in ok]):.3f} (Argon's context: Y_b 0.90-0.93 with stars); out of range: {[q[0] for q in rows if q[1] is None]}")
open(os.path.join(HERE, "argon_check.out"), "w").write("\n".join(OUT) + "\n")
