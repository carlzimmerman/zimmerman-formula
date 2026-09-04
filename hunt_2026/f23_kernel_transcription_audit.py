#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f23 -- WHICH KERNEL DID THE CLOSURE PROGRAM RUN, AND WHAT IS THE THEORY OF THE KERNEL THE DATA FOLLOW?

THE QUESTION (asked of the repository on 2026-09-04): "are you sure you are using MY equations in the appropriate
places -- and if the field-theory kernel is rejected by SPARC at 7.5 sigma, what exactly is the theory?"

THE ANSWER THIS FILE ESTABLISHES, EACH PART AS A CHECK THAT CAN FAIL:
  1. THE FIELD-THEORY DOCUMENT CARRIES THE RAR KERNEL EXACTLY.  THE_COMPLETION.md section 1.1 writes its Y-sector as
     the parametric pair  mu(u) = 1 - e^{-u},  x(u) = u^2/mu(u),  u = sqrt(y),  y = g_bar/a_0,  x = g_obs/a_0.
     Eliminating u gives g_obs/g_bar = 1/(1 - e^{-sqrt(y)}) = nu_RAR(y).  Identity, certified symbolically.
  2. THE CLOSURE PROGRAM FROZE A DIFFERENT FUNCTION.  FRIED_CHICKEN_SPEC item 12 ("preserve the exponential
     constitutive law ... lambda_perp = 1 - e^{-y}") and mond_compiler_2026 ("FROZEN NON-NEGOTIABLES: mu(y) = 1-e^{-y}")
     put the exponential in the AQUAL variable x = g/a_0 instead of in u = sqrt(g_bar/a_0).  mu_exp(x) = 1 - e^{-x}
     is not the framework's kernel; f21 showed SPARC rejects it.  The AeST branch then replaced it by the sharp
     mu_10(x) = x/(1+x^10)^{1/10} because mu_10 clears the Cassini quadrupole.  Neither is the framework's kernel.
  3. SPARC's verdict on all three, on one footing of code (f21's galaxy-bootstrap bins): nu_RAR fits, mu_exp is
     rejected in the transition, and mu_10 -- the closure program's sole surviving architecture's kernel -- is
     rejected by a much larger margin.
  4. WHICH KILLS SURVIVE THE CORRECTION.  The architectural kills carry their own kernel-blindness certificates
     (FC_B: lensing slip, alpha_3, matter conservation; the ledger's G13/A1/A2/A5).  The khronometric gradient
     no-go is proved here to be kernel-blind for ANY monotone kernel: Flanagan's condition W' - x W'' >= 0 is
     -x^2 mu'(x) >= 0, impossible when mu rises.  The kernel-SPECIFIC items (the Solar-System quadrupole, the
     HPI-Delta orbit law, the CCNL 'exact exponential' construction, the constraint-channel invisibility estimate)
     were computed on the wrong function and are re-scoped, and the one that matters is recomputed in 6.
  5. THE THEORY OF THE KERNEL THE DATA FOLLOW, at the non-relativistic level, in closed form:
        AQUAL:   x(mu) = [ln(1-mu)]^2 / mu ;   F(X) = 2u^4/mu(u) - u^4 - 4 I_3(u),  I_3 = int_0^u t^3/(e^t-1) dt
                 (polylogarithms Li_2..Li_4), with F -> X (Newton) and F -> (2/3) X^{3/2} (deep MOND).
        QUMOND:  Z = (g_bar/a_0)^2, t = Z^(1/4), Q(Z) = Z + 4 I_3(t), Q_Z = nu_RAR(sqrt(Z)).
        and the identity  nu_RAR(y) = 1 + 1/(e^{sqrt y} - 1):  the kernel is one plus a Bose-Einstein occupation
        in the deep-MOND acceleration sqrt(g_bar a_0), with a_0 as the scale.  (An identity, not a derivation.)
     Health: mu in (0,1), mu' > 0, (x mu)' > 0 (elliptic, no static ghost), Newtonian tail 1 - mu = e^{-sqrt(x mu)}.
  6. THE GATE THAT MATTERS FOR THAT THEORY: in any modified-gravity (AQUAL/QUMOND) realisation the Galactic external
     field induces a Solar-System quadrupole Q_2 = (3/2) q(eta) a_0^{3/2}/sqrt(GM_sun) (Desmond, Hees & Famaey 2024
     eq. 10, the repository's frozen convention).  It is computed here for the framework's OWN kernel with the
     committed DHF integral, against the Park 2026 two-sigma ceiling 5.2e-27 s^-2, both footings, g_ext +/- 1 sigma.

Nothing here is a relativistic completion.  It is the correction of a transcription, the closed-form
non-relativistic theory of the kernel that survives, and the one Solar-System number that theory must face.

ACTION/STATISTICAL AUDIT 2026-09-04: section 5c now uses the SQUARED-gradient action argument Z.
The former dilogarithm was an antiderivative of nu(s) in s, not the required QUMOND action primitive.
See closure_2026/two_kernel_orbit_shape_2026/ for the explicit variation, Dirac block, and falsifier.
Section 3's diagonal-bin 'sigma' labels are conditional standardized residuals, not calibrated rejection
significances. The paired galaxy/a0-profile audit there is the controlling statistical scope correction.
The quadrupole integral in section 6 is a QUMOND calculation; AQUAL does not share it exactly in general.
"""
import os, sys, math, subprocess, re, warnings
import numpy as np
warnings.filterwarnings("ignore")      # scipy/numpy warnings print absolute paths; keep them out of the .out
import sympy as sp
import mpmath as mp
from scipy import integrate
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *

ck = Check()
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CL = os.path.join(ROOT, "qwen_claude_field_theory", "closure_2026")
COMPLETION = os.path.join(ROOT, "opus_48_extended_research", "papers", "THE_COMPLETION.md")

P("=" * 118)
P("f23 -- which kernel the closure program ran, and the theory of the kernel the data follow")
P("=" * 118)

# ============================================================================================ 1. the identity
P("\n1.  THE FIELD-THEORY DOCUMENT'S KERNEL IS nu_RAR -- symbolic identity")
P("-" * 118)
u = sp.symbols("u", positive=True)
mu_u = 1 - sp.exp(-u); x_u = u**2/mu_u; y_u = u**2
ratio = sp.simplify(x_u/y_u - 1/(1 - sp.exp(-sp.sqrt(y_u))))
txt = open(COMPLETION, encoding="utf-8").read()
has_param = ("u = \\sqrt{y}" in txt or "u = \\sqrt{y}" in txt.replace("\\,", "")) and "1 - e^{-u}" in txt
info("THE_COMPLETION.md 1.1: 'mu(u) = 1 - e^{-u}, x(u) = u^2/mu(u), u = sqrt(y), x = g_obs/a_0'  found: %s" % has_param)
ck("1a THE_COMPLETION.md writes its MOND sector as the parametric pair in u = sqrt(g_bar/a_0), and that pair is "
   "EXACTLY nu_RAR(y) = 1/(1 - e^{-sqrt y}): g_obs/g_bar = x/y = 1/(1 - e^{-u}).  The framework's field-theory "
   "document carries the framework's kernel", has_param and ratio == 0, f"sympy residual x/y - nu_RAR = {ratio}")

# ============================================================================================ 2. three kernels in x
P("\n2.  THREE KERNELS AS FUNCTIONS OF THE AQUAL VARIABLE x = g/a_0")
P("-" * 118)
def mu_rar_x(x):
    """the framework's kernel in AQUAL form: 1 - mu = exp(-sqrt(x mu)), solved on (0,1)."""
    x = np.atleast_1d(np.asarray(x, float)); out = np.empty_like(x)
    for i, xx in enumerate(x):
        if xx < 1e-12: out[i] = 0.0; continue
        h = lambda m: 1.0 - m - math.exp(-math.sqrt(xx*m))
        out[i] = brentq(h, 1e-15, 1 - 1e-16, xtol=1e-15)
    return out if out.size > 1 else float(out[0])
def mu_exp_x(x): return 1.0 - np.exp(-np.asarray(x, float))
def mu_10_x(x): x = np.asarray(x, float); return x/(1 + x**10)**0.1
def nu_rar(y): y = np.maximum(np.asarray(y, float), 1e-14); return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_of_mu(mu_fun):
    """spherical inverse partner: solve x mu(x) = y for x, return x/y."""
    def f(y):
        y = np.atleast_1d(np.asarray(y, float)); out = np.empty_like(y)
        for i, yy in enumerate(y):
            if yy > 300: out[i] = 1.0; continue
            g = lambda x: x*float(mu_fun(x)) - yy
            out[i] = brentq(g, 1e-14, yy + 60.0, xtol=1e-14)/yy
        return out if out.size > 1 else float(out[0])
    return f
nu_muexp = nu_of_mu(mu_exp_x); nu_mu10 = nu_of_mu(mu_10_x)
ck("2a the AQUAL-form solve of the framework's kernel reproduces nu_RAR when pushed back to the y variable "
   "(the two representations are one function)",
   max(abs(float(nu_of_mu(mu_rar_x)(yy))/float(nu_rar(yy)) - 1) for yy in (1e-3, 0.1, 1.0, 10.0, 100.0)) < 1e-8,
   "agreement to 1e-8 over y = 1e-3..100")
P(f"    {'x = g/a0':>9} {'mu_RAR':>8} {'mu_exp':>8} {'mu_10':>8}    {'y = g_bar/a0':>12} {'nu_RAR':>8} {'nu_muexp':>9} {'nu_mu10':>8}")
for xx, yy in zip((0.3, 0.5, 1.0, 2.0, 5.0, 10.0), (0.1, 0.3, 1.0, 2.0, 5.0, 10.0)):
    P(f"    {xx:9.2f} {float(mu_rar_x(xx)):8.4f} {float(mu_exp_x(xx)):8.4f} {float(mu_10_x(xx)):8.4f}    "
      f"{yy:12.2f} {float(nu_rar(yy)):8.4f} {float(nu_muexp(yy)):9.4f} {float(nu_mu10(yy)):8.4f}")
yg = np.logspace(-3, 3, 241)
d_exp = np.abs(np.log10(nu_rar(yg)) - np.log10(nu_muexp(yg))); d_10 = np.abs(np.log10(nu_rar(yg)) - np.log10(nu_mu10(yg)))
info(f"max |dlog g_obs| vs nu_RAR:  mu_exp {d_exp.max():.3f} dex at y = {yg[d_exp.argmax()]:.2f};   mu_10 {d_10.max():.3f} dex at y = {yg[d_10.argmax()]:.2f}")
ck("2b the closure program's two frozen kernels are different functions from the framework's: mu_exp departs by "
   "> 0.05 dex and mu_10 by > 0.15 dex in predicted g_obs, both in the transition (the RAR's own scatter is 0.06)",
   d_exp.max() > 0.05 and d_10.max() > 0.15, f"{d_exp.max():.3f} / {d_10.max():.3f} dex")

# ============================================================================================ 3. SPARC on all three
P("\n3.  SPARC: the data against all three kernels (f21's galaxy-bootstrap bins, both footings)")
P("-" * 118)
gals = load_sparc()
gb = np.concatenate([g["gbar"] for g in gals]); go = np.concatenate([g["gobs"] for g in gals])
gid = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(gals)])
m = (gb > 0) & (go > 0); gb, go, gid = gb[m], go[m], gid[m]; lo = np.log10(go)
SP = {}
for foot, a0 in A0.items():
    ly = np.log10(gb/a0); edges = np.linspace(-2.6, 1.6, 22); cen = 0.5*(edges[1:] + edges[:-1]); rows = []
    for i in range(len(cen)):
        k = (ly >= edges[i]) & (ly < edges[i+1])
        if k.sum() < 15: continue
        rng = np.random.default_rng(i); gl = np.unique(gid[k]); bb = []
        for b in range(200):
            pick = rng.choice(gl, len(gl), replace=True); idx = np.concatenate([np.where(k & (gid == g_))[0] for g_ in pick]); bb.append(np.median(lo[idx]))
        rows.append((cen[i], float(np.median(lo[k])), float(np.std(bb)), int(k.sum()), float(np.median(np.log10(gb[k])))))
    rows = np.array(rows); yb = 10**rows[:, 0]
    preds = {"nu_RAR": np.log10(nu_rar(yb)) + rows[:, 4], "mu_exp": np.log10(nu_muexp(yb)) + rows[:, 4], "mu_10": np.log10(nu_mu10(yb)) + rows[:, 4]}
    chi = {k: float(np.sum(((rows[:, 1] - v)/rows[:, 2])**2)) for k, v in preds.items()}
    tr = (rows[:, 0] > -1.0) & (rows[:, 0] < 0.8)
    worst = {k: float(np.max(np.abs((rows[tr, 1] - v[tr])/rows[tr, 2]))) for k, v in preds.items()}
    SP[foot] = dict(rows=rows, chi=chi, worst=worst, dof=len(rows))
    P(f"  --- {foot}, {len(rows)} bins ---")
    P(f"    {'log y':>7} {'N':>5} {'<log g_obs>':>12} {'s.e.':>6} {'pull RAR':>9} {'pull exp':>9} {'pull mu10':>10}")
    for r_, a, b, c in zip(rows, preds["nu_RAR"], preds["mu_exp"], preds["mu_10"]):
        P(f"    {r_[0]:7.2f} {int(r_[3]):5d} {r_[1]:12.3f} {r_[2]:6.3f} {(r_[1]-a)/r_[2]:+9.1f} {(r_[1]-b)/r_[2]:+9.1f} {(r_[1]-c)/r_[2]:+10.1f}")
    info(f"chi^2 on {len(rows)} bins: nu_RAR {chi['nu_RAR']:.1f}, mu_exp {chi['mu_exp']:.1f}, mu_10 {chi['mu_10']:.1f}; "
         f"worst transition pull: RAR {worst['nu_RAR']:.1f}, exp {worst['mu_exp']:.1f}, mu_10 {worst['mu_10']:.1f} sigma")
c = SP["canonical"]
ck("3a SPARC follows nu_RAR (calibration, it was fitted to these data): chi^2/dof < 3", c["chi"]["nu_RAR"]/c["dof"] < 3, f"{c['chi']['nu_RAR']/c['dof']:.2f}")
ck("3b f21 fixed-input diagnostic reproduced: diagonal-bin difference >100 and standardized residual >5; not a calibrated rejection significance",
   c["chi"]["mu_exp"] - c["chi"]["nu_RAR"] > 100 and c["worst"]["mu_exp"] > 5, f"dchi^2 = {c['chi']['mu_exp'] - c['chi']['nu_RAR']:.0f}, worst {c['worst']['mu_exp']:.1f} sigma")
ck("3c the fixed-input diagonal-bin discrepancy is larger for mu_10 than for mu_exp on both footings; "
   "the statistic does not profile galaxy nuisance parameters or establish a global model-rejection significance",
   all(SP[f]["chi"]["mu_10"] - SP[f]["chi"]["nu_RAR"] > 3*(SP[f]["chi"]["mu_exp"] - SP[f]["chi"]["nu_RAR"]) and SP[f]["worst"]["mu_10"] > 10 for f in SP),
   "; ".join(f"{f}: dchi^2 = {SP[f]['chi']['mu_10'] - SP[f]['chi']['nu_RAR']:.0f}, worst pull {SP[f]['worst']['mu_10']:.0f} sigma" for f in SP))

# ============================================================================================ 4. what the closure program ran
P("\n4.  INVENTORY: which closure files froze which kernel, and which kills are kernel-blind")
P("-" * 118)
PATS = {"mu_exp in x": re.compile(r"1(\.0)?\s*-\s*(np|sp|math)?\.?exp\(\s*-\s*[xy]\s*\)|expm1\(\s*-\s*[xy]\s*\)"),
        "mu_10 / mu_n": re.compile(r"\(1\s*\+\s*[xy]\s*\*\*\s*(10|n)\)|mu_10|mu_n\(")}
hits = {k: [] for k in PATS}
for dp, dn, fn in os.walk(CL):
    for f in fn:
        if not f.endswith(".py"): continue
        try: s = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
        except Exception: continue
        for k, pat in PATS.items():
            if pat.search(s): hits[k].append(os.path.relpath(os.path.join(dp, f), CL))
for k, v in hits.items():
    info(f"{k}: {len(v)} closure scripts");
    for f in sorted(v)[:14]: info(f"      {f}")
    if len(v) > 14: info(f"      ... and {len(v) - 14} more")
spec = open(os.path.join(CL, "FRIED_CHICKEN_SPEC.md"), encoding="utf-8").read()
comp = open(os.path.join(CL, "mond_compiler_2026", "compiler.py"), encoding="utf-8").read()
ck("4a the substitution is documented at its source: the spec's item 12 freezes 'lambda_perp = 1 - e^{-y}' and the "
   "compiler's FROZEN NON-NEGOTIABLES freeze 'mu(y) = 1 - e^{-y}' with y = g/a_0 -- the exponential of the field "
   "theory's u = sqrt(g_bar/a_0) moved into the AQUAL variable",
   "1 − e^{−y}" in spec and "mu(y) = 1 - e^{-y}" in comp and "y = g/a0" in comp, f"{len(hits['mu_exp in x'])} scripts carry mu_exp(x), {len(hits['mu_10 / mu_n'])} carry mu_10/mu_n")
# the kernel-blindness certificate, re-run live
cert = os.path.join(CL, "fried_chicken_final", "FC_B_kernel_blindness_cert.py")
rc_cert = "n/a"
try:
    r = subprocess.run([sys.executable, cert], capture_output=True, text=True, timeout=600)
    cert_ok = r.returncode == 0; cert_txt = r.stdout; rc_cert = r.returncode
except Exception as e:
    cert_ok, cert_txt = False, str(e)
npass = len(re.findall(r"PASS|== 0|residual.*0\b", cert_txt))
ck("4b the architectural kills carry a live kernel-blindness certificate: FC_B (lensing slip Phi = 0, alpha_3 = -1, "
   "matter non-conservation) re-runs green now, so swapping mu_exp for the framework's kernel cannot revive those "
   "architectures", cert_ok, f"rc = {rc_cert}, {npass} certificate lines")
# khronometric gradient no-go for ANY monotone kernel
xs = sp.symbols("x", positive=True); muf = sp.Function("mu")(xs)
Wp = xs*muf; Wpp = sp.diff(Wp, xs); Gk = sp.simplify(Wp - xs*Wpp)
info(f"Flanagan gradient condition G = W' - x W'' with W' = x mu(x):  G = {Gk}")
dmu = np.gradient(mu_rar_x(np.logspace(-3, 2, 400)), np.logspace(-3, 2, 400))
ck("4c the khronometric no-go is kernel-blind: G = -x^2 mu'(x) for ANY kernel, so Flanagan's gradient condition G >= 0 "
   "requires mu' <= 0, impossible for a rising kernel; the framework's kernel rises everywhere, so that kill transfers",
   sp.simplify(Gk + xs**2*sp.diff(muf, xs)) == 0 and np.all(dmu > 0), "symbolic identity holds; mu_RAR' > 0 on x = 1e-3..1e2")
info("kernel-SPECIFIC items computed on mu_exp(x) and re-scoped by this file: exact_exponential_aqual_q2 (Solar-System Q2),")
info("  hpi_delta orbit law, ccnl B4 'f_exp gives mu = 1-e^{-y} EXACTLY', cde_l4c constraint-channel invisibility estimate,")
info("  FC-AeST's Cassini selection of mu_10.  The quadrupole is recomputed for the framework's kernel in section 6.")

# ============================================================================================ 5. the theory of the RAR kernel
P("\n5.  THE NON-RELATIVISTIC THEORY OF THE KERNEL THE DATA FOLLOW, IN CLOSED FORM")
P("-" * 118)
# (a) AQUAL x(mu)
mus = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 0.99])
x_of_mu = np.log(1 - mus)**2/mus
ck("5a AQUAL closed form: x(mu) = [ln(1 - mu)]^2/mu inverts the framework's kernel exactly",
   max(abs(float(mu_rar_x(xx)) - mm) for xx, mm in zip(x_of_mu, mus)) < 1e-10, "residual < 1e-10 at six points")
# (b) AQUAL F(X): F(u) = 2u^4/mu(u) - u^4 - 4 I_3(u), I_3 = int_0^u t^3/(e^t-1) dt, closed in Li_2..Li_4
mp.mp.dps = 30
def I3(uu):
    uu = mp.mpf(uu); z = mp.e**(-uu)
    return uu**3*mp.log(1 - z) - 3*uu**2*mp.polylog(2, z) - 6*uu*mp.polylog(3, z) - 6*mp.polylog(4, z) + mp.pi**4/15
def F_of_u(uu):
    uu = mp.mpf(uu); mu_ = 1 - mp.e**(-uu)
    return 2*uu**4/mu_ - uu**4 - 4*I3(uu)
def x_of_u(uu): uu = mp.mpf(uu); return uu**2/(1 - mp.e**(-uu))
# check dF/dX = mu numerically: dF/dX = (dF/du)/(dX/du), X = x^2
res = []
for uu in (0.05, 0.3, 1.0, 2.0, 4.0, 8.0):
    h = mp.mpf(1e-6)
    dF = (F_of_u(uu + h) - F_of_u(uu - h))/(2*h); dX = (x_of_u(uu + h)**2 - x_of_u(uu - h)**2)/(2*h)
    res.append(abs(float(dF/dX) - (1 - math.exp(-uu))))
i3_quad = integrate.quad(lambda t: t**3/(math.exp(t) - 1), 0, 2.0)[0]
ck("5b AQUAL Lagrangian: F(X) = 2u^4/mu - u^4 - 4 I_3(u) with I_3 in polylogarithms satisfies dF/dX = mu(x) to 1e-8 "
   "at six points, and I_3's closed form matches direct quadrature", max(res) < 1e-8 and abs(float(I3(2.0)) - i3_quad) < 1e-10,
   f"max |dF/dX - mu| = {max(res):.1e}; I_3(2) closed {float(I3(2.0)):.10f} vs quad {i3_quad:.10f}")
lim_N = float(F_of_u(40.0))/float(x_of_u(40.0))**2; lim_D = float(F_of_u(1e-3))/(float(x_of_u(1e-3))**2)**1.5
ck("5c F has the two required limits: F -> X (Newton, coefficient 1, up to the additive constant -4 pi^4/15 that the "
   "F(0) = 0 normalisation leaves at large X) and F -> (2/3) X^{3/2} (deep MOND)",
   abs(lim_N - 1) < 1e-4 and abs(lim_D - 2/3) < 2e-3, f"F/X at x = {float(x_of_u(40.0)):.0f}: {lim_N:.6f};  F/X^1.5 at x = {float(x_of_u(1e-3)):.1e}: {lim_D:.4f}")
# (c) Standard QUMOND action argument Z = |grad chi|^2/a0^2, NOT |grad chi|/a0.
def Q_of_Z(ZZ):
    ZZ = mp.mpf(ZZ)
    if ZZ == 0: return mp.mpf(0)
    return ZZ + 4*I3(ZZ**mp.mpf('0.25'))
resq = []
for ZZ in (1e-3, 0.03, 0.3, 1.0, 3.0, 30.0):
    h = mp.mpf(ZZ)*mp.mpf('1e-5')
    resq.append(abs(float((Q_of_Z(mp.mpf(ZZ)+h)-Q_of_Z(mp.mpf(ZZ)-h))/(2*h)) - float(nu_rar(math.sqrt(ZZ)))))
ck("5d QUMOND action primitive: Q(Z)=Z+4 I_3(Z^(1/4)), Z=|grad chi|^2/a0^2, has Q_Z=nu_RAR(sqrt Z); "
   "Q(0)=0, Q~(4/3) Z^(3/4) deep, Q~Z Newtonian",
   max(resq) < 1e-8 and Q_of_Z(0) == 0 and abs(float(Q_of_Z(1e-6))/((4/3)*1e-6**.75)-1) < .02 and abs(float(Q_of_Z(1e4))/1e4-1) < .03,
   f"max |Q_Z - nu(sqrt Z)| = {max(resq):.1e}; deep ratio = {float(Q_of_Z(1e-6))/((4/3)*1e-6**.75):.4f}; Newton ratio = {float(Q_of_Z(1e4))/1e4:.4f}")
# (d) Bose-Einstein identity
ys = sp.symbols("y", positive=True)
ck("5e the identity nu_RAR(y) = 1 + 1/(e^{sqrt y} - 1): the kernel is one plus a Bose-Einstein occupation number in "
   "the deep-MOND acceleration sqrt(g_bar a_0) at the scale a_0 (an identity; the temperature normalisation is a "
   "convention and NO Lambda coincidence is claimed from it)",
   sp.simplify(1/(1 - sp.exp(-sp.sqrt(ys))) - (1 + 1/(sp.exp(sp.sqrt(ys)) - 1))) == 0, "sympy residual 0")
# (e) health + tail
xg = np.logspace(-3, 3, 600); mg = mu_rar_x(xg); xm = xg*mg
ck("5f static AQUAL constitutive ellipticity: 0 < mu < 1, mu rising, (x mu) rising across six decades; "
   "this is not a dynamical ghost-freedom test", np.all((mg > 0) & (mg < 1)) and np.all(np.diff(mg) > 0) and np.all(np.diff(xm) > 0), "all three hold on x = 1e-3..1e3")
for nm, xx in (("wide binary (x ~ 1)", 1.0), ("Neptune (x ~ 7e4)", 7e4), ("Saturn (x ~ 7e5)", 7e5)):
    mm = float(mu_rar_x(min(xx, 5e3))) if xx <= 5e3 else 1.0
    tail = math.exp(-math.sqrt(xx)) if xx > 5e3 else 1 - mm
    info(f"Newtonian tail 1 - mu = e^{{-sqrt(x mu)}} at {nm}: {tail:.2e}   (mu_exp there: {math.exp(-xx):.1e})")

# ============================================================================================ 6. the Cassini quadrupole for the RAR kernel
P("\n6.  THE SOLAR-SYSTEM QUADRUPOLE FOR THE FRAMEWORK'S OWN KERNEL (modified-gravity form; DHF24 eq. 10, committed integral)")
P("-" * 118)
GM_SUN = 6.6743e-11*1.98892e30
GEXT, SGEXT = 2.32e-10, 0.16e-10               # Gaia EDR3 solar-circle field, DHF24 sec 3.3 (the OBSERVED field)
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27   # Park+2026 two-sigma ceiling, central, sigma
PREF = lambda a0: 1.5*a0**1.5/math.sqrt(GM_SUN)
def solve_eN(nu, etilde):
    """Newtonian external field e_N with nu(e_N) e_N = etilde (etilde = observed g_ext/a_0)."""
    return brentq(lambda e: float(np.asarray(nu(e)).ravel()[0])*e - etilde, 1e-9, etilde*1.5, xtol=1e-14)
def q_direct2D(nu, etilde, vmax=400.0):
    """Committed DHF integral (route1B_monotone_escape_2026.py): q = 1.5 Int Int (nu-1) N N over (v, mu)."""
    eN = solve_eN(nu, etilde)
    def ig(mu, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*mu
        if D <= 0: return 0.0
        nv = float(np.asarray(nu(math.sqrt(D))).ravel()[0])
        return (nv - 1.0)*(eN*(3*mu - 5*mu**3) + v*v*(1 - 3*mu*mu))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0, epsabs=1e-12, epsrel=1e-10)
    return abs(1.5*val), eN            # magnitude: the repository's convention is |Q2| = (3/2)|q| a0^1.5/sqrt(GM) against the positive ceiling
q_anchor, _ = q_direct2D(nu_rar, 2.0)
ck("6a the committed anchor reproduces: q(eta = 2) for the framework's kernel ('Route A' in the AeST scripts) = 0.221",
   abs(q_anchor - 0.221) < 0.003, f"q(2) = {q_anchor:.4f}")
Q2 = {}
for foot, a0 in A0.items():
    P(f"  --- {foot} footing, a_0 = {a0:.3e}: eta_solar = g_ext/a_0 = {GEXT/a0:.3f}, Q2 pass needs q < {Q2_CEIL/PREF(a0):.4f} ---")
    P(f"    {'kernel':12s} {'q(solar)':>9s} {'Q2 [s^-2]':>11s} {'Q2/ceiling':>11s} {'sigma above Park central':>25s}")
    for nm, nu in (("nu_RAR", nu_rar), ("mu_exp", nu_muexp), ("mu_10", nu_mu10)):
        q, eN = q_direct2D(nu, GEXT/a0); Q = q*PREF(a0)
        Q2[(foot, nm)] = (q, Q, Q/Q2_CEIL)
        P(f"    {nm:12s} {q:9.4f} {Q:11.3e} {Q/Q2_CEIL:11.2f} {(Q - Q2_CEN)/Q2_SIG:25.1f}")
    for dg, lab in ((-SGEXT, "g_ext - 1 sigma"), (+SGEXT, "g_ext + 1 sigma")):
        q, _ = q_direct2D(nu_rar, (GEXT + dg)/a0); Q2[(foot, lab)] = (q, q*PREF(a0), q*PREF(a0)/Q2_CEIL)
        info(f"nu_RAR at {lab}: q = {q:.4f}, Q2/ceiling = {q*PREF(a0)/Q2_CEIL:.2f}")
ck("6b anchors: mu_exp lands at the committed 3.76x ceiling (canonical) and mu_10 clears it (< 0.2x), so this is the "
   "same integral the closure program used",
   abs(Q2[("canonical", "mu_exp")][2] - 3.76) < 0.15 and Q2[("canonical", "mu_10")][2] < 0.2,
   f"mu_exp {Q2[('canonical', 'mu_exp')][2]:.2f}x, mu_10 {Q2[('canonical', 'mu_10')][2]:.3f}x")
ck("6c (HYPOTHESIS CHECK -- a FAIL is the result) the RAR kernel's QUMOND integral clears the stated "
   "Park 2026 two-sigma ceiling on at least one footing at g_ext - 1 sigma. This calculation does not establish "
   "the same quadrupole in every AQUAL or relativistic realisation",
   any(Q2[(f, "g_ext - 1 sigma")][2] < 1.0 for f in A0),
   "; ".join(f"{f}: {Q2[(f, 'nu_RAR')][2]:.2f}x central, {Q2[(f, 'g_ext - 1 sigma')][2]:.2f}x at g_ext - 1 sigma" for f in A0))
ck("6d and the exclusion is not a footing choice: on both footings the framework's kernel sits above the ceiling by "
   "more than 2x even at g_ext - 1 sigma", all(Q2[(f, "g_ext - 1 sigma")][2] > 2.0 for f in A0),
   "; ".join(f"{f}: {Q2[(f, 'g_ext - 1 sigma')][2]:.2f}x" for f in A0))

# ============================================================================================ 7. verdict
P("\n" + "=" * 118)
P("7.  VERDICT")
P("=" * 118)
P("  The field-theory document carries the framework's kernel (nu_RAR) exactly.  The closure program that built and")
P("  killed every relativistic candidate froze a different function, mu_exp(x) = 1 - e^{-x}, and its surviving branch")
P("  then selected mu_10 on Cassini. Fixed-input diagonal-bin diagnostics prefer nu_RAR; calibrated rejection is uncomputed. The reported architectural certificates are kernel-blind")
P("  by their own certificates and by the identity G = -x^2 mu', so they stand for the framework's kernel too.  The")
P("  kernel-SPECIFIC selection of mu_10 is void.")
P("  The theory of the kernel the data follow exists at the non-relativistic level in closed form (section 5): AQUAL with")
P("  F(X) in polylogarithms, or QUMOND with Q(Z)=Z+4 I_3(Z^(1/4)); nu_RAR = 1 + Bose-Einstein occupation in sqrt(g_bar a_0).")
P("  Its static constitutive sector is elliptic; dynamical ghost freedom is not established. In the QUMOND integral the Galactic external field")
P(f"  gives the Solar System a quadrupole of {Q2[('canonical', 'nu_RAR')][2]:.1f}x (canonical) / {Q2[('alt', 'nu_RAR')][2]:.1f}x (alt) the Park 2026 ceiling,")
P(f"  still {Q2[('canonical', 'g_ext - 1 sigma')][2]:.1f}x / {Q2[('alt', 'g_ext - 1 sigma')][2]:.1f}x at g_ext - 1 sigma.  That is Desmond, Hees & Famaey 2024 on this framework's numbers.")
P("  Modified inertia has no such quadrupole (the planets move at accelerations far above a_0 in a field that is not a")
P("  field equation), which is the same side of the fork the disc curl sign (f16-f18) points to -- and modified inertia")
P("  has no local action by Milgrom's theorem and every written completion of it in this repository has failed.")
P("  The QUMOND quadrupole exceeds the stated ceiling. AQUAL requires its own non-spherical solve; this integral is not an exhaustive no-go.")
P("  The RAR and exact-exponential targets remain distinct. Kernel-specific gates must be rerun for whichever explicit action is pursued.")
sys.exit(ck.done())
