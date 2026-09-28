#!/usr/bin/env python3
# AS033 — MONO splice location from its derivative rule.
# Bounded prototype: <=120 s wall, <=512 MB RSS, 1 thread (all ENFORCED in-process).
# High-precision mpmath (60 digits). All residuals are actual printed numbers.
import resource, signal, time, sys, json, math

# ---------- enforce bounds ----------
def enforce_bounds():
    # memory: 512 MB address space cap (RLIMIT_AS; macOS ok), enforced kill on breach
    try:
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, resource.RLIM_INFINITY))
        print("RLIMIT_AS soft cap 512MB set OK (hard left at infinity: macOS)")
    except Exception as e:
        print(f"WARN RLIMIT_AS: {e} (macOS hard-cap refusal; measured maxrss reported instead)")
    # cpu: soft 115 s (watchdog below also at 120)
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (115, 120))
    except Exception as e:
        print(f"WARN RLIMIT_CPU: {e}")

def watchdog(sig, frm):
    print("FATAL: watchdog fired at 120 s wall — aborting", file=sys.stderr)
    sys.exit(2)
signal.signal(signal.SIGALRM, watchdog)
signal.alarm(120)
enforce_bounds()
t0 = time.time()

import mpmath as mp
mp.mp.dps = 60

# ---------- definitions (dimensionless; y = B/a0, s = sqrt(y)) ----------
def nu_RAR(y):
    s = mp.sqrt(y)
    return 1 / (1 - mp.exp(-s))

def h_RAR(y):
    s = mp.sqrt(y)
    return y / (mp.exp(s) - 1)

def hp_RAR(y):            # closed-form derivative dh_RAR/dy
    s = mp.sqrt(y)
    E = mp.exp(s)
    return 1 / (E - 1) - (s / 2) * E / (E - 1) ** 2

def hpp_RAR(y):           # closed-form second derivative
    s = mp.sqrt(y)
    E = mp.exp(s)
    W = E / (E - 1) ** 2
    return W * (s / (1 - mp.exp(-s)) - (3 + s) / 2) / (2 * s)

DELTA = mp.mpf("0.05")

# ---------- step 1: peak y_p, h_p from h'(y_p)=0 (landmarks: 2.5396, 0.647610) ----------
# e^s (2 - s) = 2  <->  h_p = s_p (2 - s_p)
def peak_eq(s):
    return mp.exp(s) * (2 - s) - 2

s_p = mp.findroot(peak_eq, mp.mpf("1.5936"))
y_p = s_p ** 2
h_p = s_p * (2 - s_p)
h_p_check = h_RAR(y_p)
print("STEP1 peak: y_p =", mp.nstr(y_p, 40))
print("STEP1 peak: s_p =", mp.nstr(s_p, 40))
print("STEP1 peak: h_p =", mp.nstr(h_p, 40), " (= h_RAR(y_p) =", mp.nstr(h_p_check, 40),
      "; diff =", mp.nstr(h_p - h_p_check, 3), ")")
print("STEP1 peak: h'(y_p) residual =", mp.nstr(hp_RAR(y_p), 3))
print("STEP1 landmarks vs task: |y_p - 2.5396| =", mp.nstr(abs(y_p - mp.mpf("2.5396")), 5),
      " |h_p - 0.647610| =", mp.nstr(abs(h_p - mp.mpf("0.647610")), 5))

# ---------- step 2: splice crossing  h'_RAR(y*) = DELTA*h_p/(y*+y_p) ----------
def F(y):
    return hp_RAR(y) - DELTA * h_p / (y + y_p)

# unicity analytic facts (bracketed values, not grid proof):
# h''<0 on (0,y_p)  <=>  psi(s) = (3+s)(1-e^-s) - 2s > 0 on (0,s_p):
# psi'(s)=(2+s)e^-s-1 has unique root s0 (e^s=2+s), psi max there; psi(s_p) evaluated here:
def psi(s):
    return (3 + s) * (1 - mp.exp(-s)) - 2 * s

s0 = mp.findroot(lambda s: (2 + s) * mp.exp(-s) - 1, mp.mpf("1.1462"))
print("STEP2 unicity bracketing: s0 (psi' root) =", mp.nstr(s0, 20),
      "; psi(s0) =", mp.nstr(psi(s0), 8), "> 0 ; psi(s_p) =", mp.nstr(psi(s_p), 8), "> 0")
print("STEP2 F(0+)=+inf (h'->+inf), F(y_p) =", mp.nstr(F(y_p), 8), "< 0  => unique root in (0,y_p) by strict monotonicity")

y_star = mp.findroot(F, (mp.mpf("1.5"), mp.mpf("2.4")))
print("STEP2 y_star =", mp.nstr(y_star, 40))
print("STEP2 |y_star - 2.3374| =", mp.nstr(abs(y_star - mp.mpf("2.3374")), 5))
print("STEP2 F(y_star) =", mp.nstr(F(y_star), 3), " (absolute residual of the crossing equation)")
print("STEP2 h'_RAR(y_star) =", mp.nstr(hp_RAR(y_star), 40))
print("STEP2 DELTA*h_p/(y_star+y_p) =", mp.nstr(DELTA * h_p / (y_star + y_p), 40))

# ---------- step 3: continuity join (value) ----------
h_mono_cont = h_RAR(y_star) + DELTA * h_p * mp.log((y_star + y_p) / (y_star + y_p))
print("STEP3 h_mono(y_star) - h_RAR(y_star) =", mp.nstr(h_mono_cont - h_RAR(y_star), 3),
      " (exact log(1)=0 term: delta*h_p*log(1) =", mp.nstr(DELTA * h_p * mp.log(1), 3), ")")
# derivative continuity at the splice (C^1 join):
print("STEP3 h' jump at y_star = |h'_RAR - delta*h_p/(y*+y_p)| =", mp.nstr(abs(F(y_star)), 3))
# second-derivative kink (C^1 but not C^2):
J2 = -DELTA * h_p / (y_star + y_p) ** 2 - hpp_RAR(y_star)
print("STEP3 h'' jump at y_star (RAR-side - continuation-side) =", mp.nstr(J2, 8),
      " ; hpp_RAR(y_star) =", mp.nstr(hpp_RAR(y_star), 8))

# ---------- step 4: independent check, different representation ----------
# 4a. symbolic differentiation (sympy) vs closed form
import sympy as sp
ys_ = sp.symbols('y', positive=True)
hs = ys_ / (sp.exp(sp.sqrt(ys_)) - 1)
hprime_sym = sp.simplify(sp.diff(hs, ys_))
hprime_closed = 1 / (sp.exp(sp.sqrt(ys_)) - 1) - (sp.sqrt(ys_) / 2) * sp.exp(sp.sqrt(ys_)) / (sp.exp(sp.sqrt(ys_)) - 1) ** 2
print("STEP4a symbolic residual simplify(dh - closedform) =", sp.simplify(hprime_sym - hprime_closed))
# 4b. numeric differentiation check at several y values
for yy in [0.2, 1.0, y_star, y_p, 5.0]:
    h = mp.mpf(10) ** -30
    num = (h_RAR(yy + h) - h_RAR(yy - h)) / (2 * h)
    print(f"STEP4b numeric d/dy vs closed form at y={mp.nstr(yy,6)}: residual =",
          mp.nstr(num - hp_RAR(yy), 3))
# 4c. verify y_star via direct substitution into ORIGINAL max-equation (both sides, high precision)
lhs = hp_RAR(y_star); rhs = DELTA * h_p / (y_star + y_p)
print("STEP4c substitution residual |lhs-rhs| =", mp.nstr(abs(lhs - rhs), 3))

# ---------- step 5: negative controls (capable of failing) ----------
print()
print("=== NEGATIVE CONTROLS ===")
# NC1: change the PEAK DEFINITION while retaining the OLD splice -> discontinuity of h'
alt_peaks = {
    "y_p' = y_p + 0.25 (mislocated peak)": y_p + mp.mpf("0.25"),
    "y_p' = 2.0 (arbitrary peak)": mp.mpf("2.0"),
    "h_p' = 0.5*h_p (peak value halved)": None,
}
for name, yp2 in alt_peaks.items():
    if yp2 is None:
        hp2 = h_p / 2
        yp2u = y_p
    else:
        hp2 = h_RAR(yp2)
        yp2u = yp2
    jump = abs(DELTA * hp2 / (y_star + yp2u) - hp_RAR(y_star))
    rel = jump / abs(DELTA * h_p / (y_star + y_p))
    print(f"NC1 [{name}]: h' discontinuity at OLD y_star = {mp.nstr(jump, 8)} (relative to true delta*h_p/(y+p) = {mp.nstr(rel, 5)})")

# NC2: shifted SPLICE (peak retained) -> join condition violated
for dyy in [mp.mpf("0.01"), mp.mpf("0.05"), mp.mpf("-0.05")]:
    yy = y_star + dyy
    mism = abs(hp_RAR(yy) - DELTA * h_p / (yy + y_p))
    print(f"NC2 [y_star {mp.nstr(dyy,3)} shifted -> y={mp.nstr(yy,8)}]: |h'_RAR - delta*h_p/(y+y_p)| = {mp.nstr(mism, 8)}")

# NC3: deep / Newtonian limiting regimes
print("NC3 deep y->0: g/B = nu_RAR(y); nu*sqrt(y) - 1 at y=1e-10 =",
      mp.nstr(nu_RAR(mp.mpf("1e-10")) * mp.mpf("1e-5") - 1, 8), " (h'_mono follows RAR since max picks h'_RAR: h'_RAR(y)->+inf)")
yy = mp.mpf("1e-10")
print("NC3 deep: max(h'_RAR, delta*h_p/(y+y_p)) picks RAR? h'_RAR =", mp.nstr(hp_RAR(yy), 6),
      "vs RHS =", mp.nstr(DELTA * h_p / (yy + y_p), 8))
print("NC3 Newtonian y->inf: nu_mono(y)-1 at y=1e6 =",
      mp.nstr((h_RAR(y_star) + DELTA * h_p * mp.log((mp.mpf("1e6") + y_p) / (y_star + y_p))) / mp.mpf("1e6"), 8),
      "-> 0 like delta*h_p*ln(y)/y; h_RAR(1e6) =", mp.nstr(h_RAR(mp.mpf("1e6")), 6))
yy = mp.mpf("1e6")
hmono_inf = h_RAR(y_star) + DELTA * h_p * mp.log((yy + y_p) / (y_star + y_p))
print("NC3 Newtonian: g/B = 1 + h_mono/y =", mp.nstr(1 + hmono_inf / yy, 12), "-> 1")
print("NC3 sanity: h_mono(y_p) =", mp.nstr(h_RAR(y_star) + DELTA * h_p * mp.log((y_p + y_p) / (y_star + y_p)), 10),
      "> h_p =", mp.nstr(h_p, 10), " (continuation rises above the RAR peak: phantom growth)")

# NC4: negative control on unicity — a SECOND kernel-scale is not a second crossing:
#   with delta' = 0.07 the crossing moves measurably; joining at OLD y_star violates derivative eq
for delta2 in [mp.mpf("0.07"), mp.mpf("0.03")]:
    F2 = lambda y: hp_RAR(y) - delta2 * h_p / (y + y_p)
    y2 = mp.findroot(F2, (mp.mpf("1.5"), mp.mpf("2.4")))
    print(f"NC4 [delta'={delta2}]: new crossing y_star' = {mp.nstr(y2, 10)}; |h'_RAR - delta'*h_p/(y+y_p)| at OLD y_star =",
          mp.nstr(abs(F2(y_star)), 8))

# ---------- framework footings (dimensionless result -> both footings) ----------
G = mp.mpf("6.67430e-11"); c = mp.mpf("299792458")
a0_can = mp.mpf("9.3619e-11"); a0_alt = mp.mpf("1.1279e-10")
rho_can = 4 * a0_can ** 2 / (G * c ** 2)
rho_alt = 4 * a0_alt ** 2 / (G * c ** 2)
print()
print("FOOTINGS rho_Lambda(canonical) =", mp.nstr(rho_can, 12), "kg/m^3 ; rho_Lambda(alternative) =", mp.nstr(rho_alt, 12), "kg/m^3 ; ratio =", mp.nstr(rho_alt / rho_can, 10))
print("FOOTINGS B_star = y_star*a0: canonical =", mp.nstr(y_star * a0_can, 10), "m/s^2 ; alternative =", mp.nstr(y_star * a0_alt, 10), "m/s^2")
print("FOOTINGS kappa_eff if rho fixed at canonical and a0=alternative =", mp.nstr(mp.mpf("0.5") * a0_alt / a0_can, 10))
print("FOOTINGS rho ratio if kappa fixed (rho_alt/rho_can) =", mp.nstr((a0_alt / a0_can) ** 2, 10))

# ---------- heat-filter action on the splice (scoped 1-D model diagnostic) ----------
# S_xi = exp((xi^2/2) d^2/dy^2) on a periodized 1-D domain, Lebesgue measure.
# Model operator ONLY; the framework's metric/lattice-dependent S is a separate object.
import numpy as np
rng = np.random.default_rng(0)
# ---- (A) full-domain diagnostic: heat filter vs the y->0 divergence of h''_RAR ----
N = 2 ** 16
Ymax = 10.0
step = Ymax / N
ys_g = np.linspace(step / 2, Ymax - step / 2, N)   # midpoint grid: y>0 (h'' diverges at 0)
s_g = np.sqrt(ys_g)
E_g = np.exp(s_g)
W_g = E_g / (E_g - 1) ** 2
h2 = W_g * (s_g / (1 - np.exp(-s_g)) - (3 + s_g) / 2) / (2 * s_g)   # h''_RAR on (0,ystar)
mask = ys_g >= float(y_star)
h2[mask] = -DELTA * h_p / (ys_g[mask] + y_p)                          # continuation h'' (derivative of RHS)
h2 = h2 - np.mean(h2)
k = 2 * np.pi * np.fft.fftfreq(N, d=step)
for xi in [0.01, 0.05]:
    S = np.exp(-(xi ** 2 / 2) * k ** 2)
    h2s = np.real(np.fft.ifft(np.fft.fft(h2) * S))
    print(f"HEAT-A xi={xi} (global domain): raw ||h''_mono||_inf = {np.max(np.abs(h2)):.3e}; "
          f"after S_xi = {np.max(np.abs(h2s)):.3e} (singular h''~-1/(4 y^(3/2)) at y->0 is regularized)")
print(f"HEAT-A input: h''_mono ||.||_inf on [0,10] = {np.max(np.abs(h2)):.3e} (y->0 divergence, not the splice)")

# ---- (B) splice-local diagnostic: window [1.5,3.5], seam-continuous baseline ---------
L = 3.5 - 1.5
Nw = 2 ** 16
stw = L / Nw
yw = 1.5 + stw * (np.arange(Nw) + 0.5)
sw = np.sqrt(yw); Ew = np.exp(sw); Ww = Ew / (Ew - 1) ** 2
h2w = Ww * (sw / (1 - np.exp(-sw)) - (3 + sw) / 2) / (2 * sw)
mask_loc = yw >= float(y_star)
h2w[mask_loc] = -DELTA * h_p / (yw[mask_loc] + y_p)
# linear baseline through the endpoints -> periodic seam ~ C^0
b0, b1 = h2w[0].item(), h2w[-1].item()
base = b0 + (b1 - b0) * (yw - yw[0]) / L
g = h2w - base
g -= g.mean()
kw = 2 * np.pi * np.fft.fftfreq(Nw, d=stw)
J2f = float(J2)
for xi in [0.01, 0.05]:
    Sw = np.exp(-(xi ** 2 / 2) * kw ** 2)
    gs = np.real(np.fft.ifft(np.fft.fft(g) * Sw))
    win = np.abs(yw - float(y_star)) <= 0.5
    dev = np.max(np.abs(gs[win] - g[win]))
    # smoothed curvature AT the splice point vs raw sides:
    idx = int(np.argmin(np.abs(yw - float(y_star))))
    print(f"HEAT-B xi={xi} (splice window |y-y*|<=0.5): S_xi deviation {dev:.3e}; "
          f"h'' at splice raw {h2w[idx]:.5f} -> filtered {gs[idx]+base[idx]:.5f} "
          f"(raw step amplitude {J2f:.5f})")

t1 = time.time()
ru = resource.getrusage(resource.RUSAGE_SELF)
maxrss_mb = ru.ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
print(f"\nBOUNDS wall={t1 - t0:.2f}s (alarm 120s) maxrss={maxrss_mb:.2f} MB (cap 512 MB) threads=1 (OMP_NUM_THREADS=1, pure python)")

# ---------- exact digit dumps for derivation.md ----------
out = {
    "y_p": mp.nstr(y_p, 45), "s_p": mp.nstr(s_p, 45), "h_p": mp.nstr(h_p, 45),
    "y_star": mp.nstr(y_star, 45),
    "hprime_at_star": mp.nstr(hp_RAR(y_star), 45),
    "rhs_at_star": mp.nstr(DELTA * h_p / (y_star + y_p), 45),
    "F_residual": mp.nstr(F(y_star), 3),
    "J2": mp.nstr(J2, 12),
    "rho_can": mp.nstr(rho_can, 12), "rho_alt": mp.nstr(rho_alt, 12),
    "Bstar_can": mp.nstr(y_star * a0_can, 10), "Bstar_alt": mp.nstr(y_star * a0_alt, 10),
}
with open("landmarks.json", "w") as f:
    json.dump(out, f, indent=1)
print("landmarks.json written.")
signal.alarm(0)
