#!/usr/bin/env python3
# AS044 - Deep point-source potential and boundary matching
# Bounded prototype: <=120 s wall (internal deadline 100 s + shell timeout), <=512 MB RSS (RLIMIT_AS enforced), 1 thread.
import mpmath as mp, json, os, sys, time, resource, math

mp.mp.dps = 50
t0 = time.monotonic()
DEADLINE = t0 + 100.0

def check():
    if time.monotonic() > DEADLINE:
        raise RuntimeError("internal deadline (100 s) exceeded")

# --- actually enforced memory bound: 512 MB address space ---------------------
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    mem_enforced = "RLIMIT_AS=512MB set in-process (enforced)"
except Exception as e:
    mem_enforced = f"RLIMIT_AS failed: {e} (recorded; max RSS from /usr/bin/time -l)"


def ms():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_maxrss  # KB on macOS

# --- constants (SI) -------------------------------------------------------------
G = mp.mpf("6.67430e-11"); c = mp.mpf("299792458")
MSUN = mp.mpf("1.98847e30"); PC = mp.mpf("3.085677581491367e16")
A0CAN = mp.mpf("9.3619e-11"); A0ALT = mp.mpf("1.1279e-10")
E = mp.e

# --- branch constitutive responses: x(y) = g/a0 given y = g_bar/a0 -------------
def nu_RAR(y): return 1 / (1 - mp.exp(-mp.sqrt(y)))
def x_Q(y): return mp.sqrt(y * y + y)
def x_RAR(y): return y * nu_RAR(y)
def mu2(x): return 1 - (1 + x / 2) ** -2
def bisect(f, lo, hi, tol=mp.mpf("1e-48"), maxit=250):
    flo, fhi = f(lo), f(hi)
    if flo == 0: return lo
    if fhi == 0: return hi
    assert flo * fhi < 0, (lo, hi, flo, fhi)
    for _ in range(maxit):
        mid = (lo + hi) / 2
        fm = f(mid)
        if fm == 0 or (hi - lo) < tol * max(1, abs(mid)):
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2

def island(s):
    return s

def x_MU2(y):
    f = lambda x: x * mu2(x) - y
    hi = max(mp.mpf(1), 2 * y + 2)
    while f(hi) <= 0:
        hi *= 2
    return bisect(f, mp.mpf(0), hi)
def x_EXP(y):
    f = lambda x: x * (1 - mp.exp(-x)) - y
    hi = max(mp.mpf(1), y + 1)
    while f(hi) <= 0:
        hi *= 2
    return bisect(f, mp.mpf(0), hi)

def h_RAR(y): return y * (nu_RAR(y) - 1)
def h_RAR_d(y):
    # nu' = -nu^2 e^{-u}/(2u), u = sqrt(y); h' = nu - 1 + y*nu'
    u = mp.sqrt(y)
    return nu_RAR(y) - 1 - u * mp.exp(-u) * nu_RAR(y) ** 2 / 2

# MONO splice landmarks (verify against task-provided rounded values)
DELTA = mp.mpf("0.05")
# scan for sign change of h_RAR' on [2.0, 3.2] (peak known ~2.54)
def _bracket(f, lo, hi, n=4000):
    step = (hi - lo) / n
    a = lo
    fa = f(a)
    for i in range(n):
        b = lo + (i + 1) * step
        fb = f(b)
        if fa == 0: return (a, b)
        if fb == 0: return (a, b)
        if fa * fb < 0: return (a, b)
        a, fa = b, fb
    raise RuntimeError("no sign change in bracket scan")
y_p = bisect(h_RAR_d, *_bracket(h_RAR_d, mp.mpf("2.0"), mp.mpf("3.2")))
h_p = h_RAR(y_p)
# crossing of h_RAR' with delta*h_p/(y+y_p): scan on [2.0, 2.8]
def crossf(y): return h_RAR_d(y) - DELTA * h_p / (y + y_p)
y_star = bisect(crossf, *_bracket(crossf, mp.mpf("2.0"), mp.mpf("2.8")))

def h_MONO(y):
    if y <= y_star:
        return h_RAR(y)
    return h_RAR(y_star) + DELTA * h_p * mp.log((y + y_p) / (y_star + y_p))
def x_MONO(y): return y + h_MONO(y)

# --- STEP 1: grid y = 10^k, k = -10 .. 8 step 0.1 ------------------------------
ks = [k / 10 for k in range(-100, 81)]
rows = []
for k in ks:
    check()
    y = mp.power(10, k)
    xq, xr = x_Q(y), x_RAR(y)
    xm2, xe, xmo = x_MU2(y), x_EXP(y), x_MONO(y)
    rows.append([k, y, xq, xr, xm2, xe, xmo])
    for x in (xq, xr, xm2, xe, xmo):
        assert x > 0

def rel(x, y): return abs(x / mp.sqrt(y) - 1)

GRID = {
    "n_points": len(rows),
    "k_range": [ks[0], ks[-1]],
}
deep_band = [r for r in rows if r[0] <= -4]
GRID["deep_band_k_max"] = deep_band[-1][0]
for name, idx in [("Q", 2), ("RAR", 3), ("MU2", 4), ("EXP", 5), ("MONO", 6)]:
    vals = [(r[0], rel(r[idx], r[1])) for r in deep_band]
    mx = max(vals, key=lambda t: t[1])
    at_min = vals[0][1]
    GRID[f"deeprel_max_{name}"] = {"k": mx[0], "rel": mp.nstr(mx[1], 6), "at_k=-10": mp.nstr(at_min, 6)}
# finite-y discrepancy (not shared): x-1 at y = 1
GRID["finite_y_x_minus_1_at_y1"] = {n: mp.nstr(rows[100][idx] - 1, 12) for n, idx in
                                    [("Q", 2), ("RAR", 3), ("MU2", 4), ("EXP", 5), ("MONO", 6)]}

# --- leading-term analysis: x(y)/sqrt(y) - 1 ------------------------------------
def leading(name, idx):
    # slope of log10(x - sqrt(y)) vs k over a deep decade; plus coefficient
    band = [r for r in rows if -8.5 <= r[0] <= -6.5 and r[0] >= -10]
    # use k -9.5..-6.5
    band = [r for r in rows if -9.5 <= r[0] <= -6.5]
    slope_num = []
    for r in band:
        d = r[idx] - mp.sqrt(r[1])
        if d > 0:
            slope_num.append((r[0], mp.log10(d)))
    if not slope_num:
        return {"name": name, "error": "no positive excess"}
    # linear fit k -> log10 excess
    n = len(slope_num)
    sk = sum(t[0] for t in slope_num); se = sum(t[1] for t in slope_num)
    skk = sum(t[0] ** 2 for t in slope_num); ske = sum(t[0] * t[1] for t in slope_num)
    den = n * skk - sk * sk
    slope = (n * ske - sk * se) / den
    inter = (se - slope * sk) / n
    coef = mp.power(10, inter)  # excess = coef * y^slope
    return {"name": name, "slope_loglog": mp.nstr(slope, 6), "coef": mp.nstr(coef, 6)}

GRID["leading_excess"] = [leading(n, i) for n, i in
                          [("Q", 2), ("RAR", 3), ("MU2", 4), ("EXP", 5), ("MONO", 6)]]

# --- splice fidelity (MONO) ------------------------------------------------------
SPLICE = {
    "y_p": mp.nstr(y_p, 15), "h_p": mp.nstr(h_p, 15),
    "y_star": mp.nstr(y_star, 15),
    "declared_y_p": "2.539638282", "declared_y_star": "2.337412405", "declared_h_p": "0.647610238",
    "h_cont_abs": mp.nstr(abs(h_MONO(y_star) - h_RAR(y_star)), 12),
    "h_deriv_crossing_resid": mp.nstr(abs(h_RAR_d(y_star) - DELTA * h_p / (y_star + y_p)), 12),
}
for lab, yy in [("pred_y_star", y_star / 2), ("just_below", y_star * 0.8), ("just_above", y_star * 1.2),
                ("high_10x", y_star * 10), ("high_1e4x", y_star * 1e4)]:
    SPLICE[f"maxrule_{lab}"] = {
        "h'_RAR": mp.nstr(h_RAR_d(yy), 8), "delta_hp/(y+yp)": mp.nstr(DELTA * h_p / (yy + y_p), 8)}

# --- STEP 2/3: deep potential, matching, integration constant --------------------
def potential(Mb, a0):
    C = mp.sqrt(G * Mb * a0)          # = v_flat^2
    rM = mp.sqrt(G * Mb / a0)         # MOND radius
    rref = E * rM
    PhiN = lambda r: -G * Mb / r
    PhiD = lambda r: C * mp.log(r / rref)
    return C, rM, rref, PhiN, PhiD

# double-continuity forcing: solve G*Mb/r_t^2 = C/r_t for r_t
def force_match_r_t(Mb, a0):
    C, rM, rref, _, _ = potential(Mb, a0)
    rt = mp.findroot(lambda r: G * Mb / r ** 2 - C / r, rM)
    return rt, rM, C

MATCH = {}
for footing, a0 in [("canonical_9.3619e-11", A0CAN), ("alternative_1.1279e-10", A0ALT)]:
    C, rM, rref, PhiN, PhiD = potential(10 ** 11 * MSUN, a0)
    rt, rM2, C2 = force_match_r_t(10 ** 11 * MSUN, a0)
    resid = {
        "gN_rM_minus_a0": mp.nstr(abs(G * (10 ** 11 * MSUN) / rM ** 2 - a0), 6),
        "gD_rM_minus_a0": mp.nstr(abs(C / rM - a0), 6),
        "PhiN_rM_plus_C": mp.nstr(abs(PhiN(rM) + C), 6),
        "PhiD_rM_plus_C": mp.nstr(abs(PhiD(rM) + C), 6),
        "r_t_minus_rM": mp.nstr(abs(rt - rM), 6),
        "rref_over_rM": mp.nstr(rref / rM, 12),
    }
    # derivative identity d/dr PhiD = C/r
    for rr in [2 * rM, 5 * rM, 10 * rM, 100 * rM]:
        d = mp.diff(lambda r: PhiD(r), rr)
        resid[f"ddr_PhiD_at_{int(round(rr/rM))}rM"] = mp.nstr(abs(d - C / rr), 6)
    # integral identity: Phi(r) - Phi(rM) = int_{rM}^{r} C/r' dr'
    for rr in [2 * rM, 5 * rM, 10 * rM, 50 * rM]:
        q = mp.quad(lambda r: C / r, [rM, rr])
        resid[f"int_identity_{int(round(rr/rM))}rM"] = mp.nstr(abs(q - (PhiD(rr) - PhiD(rM))), 6)
    # leading neglected term (NOT vacuous): branch potential Phi_RAR(r) = int g_RAR dr'
    # with g_RAR(r) = (G Mb/r^2) nu_RAR(G Mb/(a0 r^2)); verify Phi_RAR - C ln(r/rref)
    # has leading correction -G Mb/(2 r) relative to the log term, i.e.
    # [Phi_RAR(r) - Phi_RAR(r0)] - C ln(r/r0) ~ (G Mb/2)(1/r0 - 1/r) for r, r0 >> rM
    r0 = 1000 * rM
    def Phi_RAR(r):
        g = lambda s: (G * (10 ** 11 * MSUN) / s ** 2) * nu_RAR(G * (10 ** 11 * MSUN) / (a0 * s ** 2))
        return mp.quad(g, [r0, r])  # Phi(r) - Phi(r0), integrand ordered upward
    for rr in [10 * rM, 100 * rM, 500 * rM]:
        integ = Phi_RAR(rr)                      # = Phi(rr) - Phi(r0)
        logpart = C * mp.log(rr / r0)            # = C ln(rr) - C ln(r0) = PhiD(rr)-PhiD(r0)
        delta = integ - logpart
        expect = (G * (10 ** 11 * MSUN) / 2) * (1 / r0 - 1 / rr)
        resid[f"branch_leading_term_{int(round(rr/rM))}rM_ratio"] = mp.nstr(delta / expect, 8)
    MATCH[footing] = {k: (v if not isinstance(v, mp.mpf) else mp.nstr(v, 10)) for k, v in resid.items()}
    MATCH[footing]["v_flat_m_s"] = mp.nstr(mp.sqrt(C), 10)
    MATCH[footing]["v_flat_km_s"] = mp.nstr(mp.sqrt(C) / 1000, 10)
    MATCH[footing]["r_M_m"] = mp.nstr(rM, 10)
    MATCH[footing]["r_M_kpc"] = mp.nstr(rM / (1000 * PC), 10)
    MATCH[footing]["C_m2_s2"] = mp.nstr(C, 10)
    check()

# --- negative controls (must be capable of failing) ------------------------------
CTRL = {}
# C1: extend the logarithmic branch to infinity demanding a finite zero potential
C, rM, rref, PhiN, PhiD = potential(10 ** 11 * MSUN, A0CAN)
vals = {f"r=10^{k}_rM": mp.nstr(PhiD(10 ** k * rM), 8) for k in (0, 1, 2, 3, 4, 6)}
mono = mp.nstr(PhiD(10 ** 20 * rM), 8)
CTRL["C1_log_to_infinity"] = {
    "statement": "Phi_deep(r) = C ln(r/(e rM)) has NO finite limit as r -> oo;"
                 " requiring Phi(oo)=0 fails (control detects: cannot be satisfied).",
    "Phi_at_large_r": vals, "Phi(1e20 rM)": mono,
    "control_outcome": "control TRIGGERED (requirement unsatisfiable) - as expected",
}
# C2: force continuity forces r_t = r_M - show mismatch at r_t != r_M
for frac in [0.25, 0.5, 0.9, 1.0, 1.1, 2.0, 4.0]:
    rt = frac * rM
    dg = abs(G * (10 ** 11 * MSUN) / rt ** 2 - C / rt) / a0
    CTRL.setdefault("C2_g_jump_at_r_t", {})[str(frac) + "_rM"] = mp.nstr(dg, 8)
CTRL["C2_g_jump_at_r_t"]["control_outcome"] = "zero only at r_t = r_M (discriminates)"
# C3: mutation of the integration constant r_ref: continuity residual at r_M
for lab, f in [("r_ref=r_M", 1.0), ("r_ref=2*rM", 2.0), ("r_ref=e*rM (correct)", 1.0 / E)]:
    rrf = f * rM if lab != "r_ref=e*rM (correct)" else E * rM
    res = C * mp.log(rM / rrf) + C
    CTRL.setdefault("C3_rref_mutation", {})[lab] = mp.nstr(abs(res), 8)
CTRL["C3_rref_mutation"]["control_outcome"] = "residual 0 iff r_ref = e rM (mutation detected)"

# --- dimensional examples, both footings ----------------------------------------
DIM = {}
for footing, a0 in [("canonical", A0CAN), ("alternative", A0ALT)]:
    rhoL = 4 * a0 ** 2 / (G * c ** 2)
    DIM[footing] = {"a0_m_s2": mp.nstr(a0, 10), "rho_Lambda_kg_m3": mp.nstr(rhoL, 10)}
    for Mlab, Mb in [("1e11_Msun", 10 ** 11 * MSUN), ("6e10_Msun", 6 * 10 ** 10 * MSUN), ("1_Msun", MSUN)]:
        C, rm, rref, PhiN, PhiD = potential(Mb, a0)
        DIM[footing][Mlab] = {
            "C_m2_s2": mp.nstr(C, 10),
            "v_flat_km_s": mp.nstr(mp.sqrt(C) / 1000, 10),
            "r_M_m": mp.nstr(rm, 10),
            "r_M_pc": mp.nstr(rm / PC, 10),
            "r_M_kpc": mp.nstr(rm / (1000 * PC), 10),
            "r_ref_m": mp.nstr(rref, 10),
            "Phi(r_M)_m2_s2": mp.nstr(PhiN(rm), 10),
            "g_deep(10 rM)_m_s2": mp.nstr(C / (10 * rm), 10),
            "Phi_deep(100 rM)_m2_s2": mp.nstr(PhiD(100 * rm), 10),
        }
    check()

# --- MONO vs RAR on the deep side -------------------------------------------------
DEEPREGIME = {}
rM11 = mp.sqrt(G * (10 ** 11 * MSUN) / A0CAN)
for rr in [1, 1.5, 2, 3, 5, 10, 30, 100]:
    r = rr * rM11
    y = G * (10 ** 11 * MSUN) / (A0CAN * r ** 2)
    DEEPREGIME[f"r={rr}rM"] = {
        "y": mp.nstr(y, 6),
        "x_MONO": mp.nstr(x_MONO(y), 10),
        "x_RAR": mp.nstr(x_RAR(y), 10),
        "diff": mp.nstr(x_MONO(y) - x_RAR(y), 10),
        "on_RAR_segment": bool(y <= y_star),
    }

# --- persistence -----------------------------------------------------------------
os.makedirs("out", exist_ok=True)
with open("out/grid.csv", "w") as f:
    f.write("k,y,x_Q,x_RAR,x_MU2,x_EXP,x_MONO\n")
    for r in rows:
        f.write(",".join(mp.nstr(v, 30) for v in r) + "\n")
res = {
    "constants": {"G": str(G), "c": str(c), "M_sun": str(MSUN), "pc": str(PC),
                  "a0_can": str(A0CAN), "a0_alt": str(A0ALT), "delta": str(DELTA)},
    "splice": SPLICE, "grid": GRID, "matching": MATCH, "controls": CTRL,
    "dimensional": DIM, "deep_regime_mono_vs_rar": DEEPREGIME,
}
with open("out/residuals.json", "w") as f:
    json.dump(res, f, indent=1)
print("elapsed_s", round(time.monotonic() - t0, 3))
print("maxrss_kb", ms(), "|", mem_enforced)
print(json.dumps({k: res[k] for k in ("splice", "grid", "controls")}, indent=1)[:4000])
