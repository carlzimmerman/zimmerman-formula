"""CFG357: the chassis's heat filter vs the EFE-induced solar-system quadrupole Q2 (Cassini), kappa = 1/2, both footings.
Solver: a COPY of p58's qumond_efe_multipole.py (sonnet55_push/puzzle_32pi/), extended by one substitution: the MOND
kernel acts on the heat-filtered field G_f = g_sun,filtered + g_Ne (L340 S1 / MASTER_LAGRANGIAN: W_b = exp((xi^2/2)Delta) U,
i.e. the Sun's mass smeared into a Gaussian of width xi), while the Sun's Newtonian field stays unfiltered:
  D = (nu(|G_f|/a0) - 1) G_f - (nu_e - 1) g_Ne    (p58: the same with G_f -> G).
Kernel nu_mono: exact reimplementation of L340 lines 104-118.  Frozen criteria: FROZEN_CRITERIA.md.
Run from the repo root: python3 campaign_fresh_gravity/CFG357_heat_filter_cassini_q2/cfg357_heat_filter_q2.py
CFG357_MUTATE=1: external field at 10% (outputs *_MUTATE.*; C1 must FAIL, rc 1).
"""
import os, sys, json, math, numpy as np
from numpy.polynomial.legendre import leggauss, legval, legder
from scipy.optimize import brentq
from scipy.special import erf
import warnings; warnings.filterwarnings("ignore")
MUT = os.environ.get("CFG357_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); TAG = "_MUTATE" if MUT else ""
GM = 4 * np.pi**2; MS2 = (3.15576e7)**2 / 1.495978707e11; YR = 3.15576e7
PC_AU = 206264.806
GE = 2.146e-10 * (0.1 if MUT else 1.0)
FOOT = {"canonical": 9.3603e-11, "alt": 1.13e-10}
Q2C, SIG = 3e-27, 3e-27
out = {"lane": "CFG357", "mutate": MUT, "ge": GE, "rows": {}, "checks": {}}
res = []
def check(n, ok, m=""):
    res.append(bool(ok)); out["checks"][n] = {"pass": bool(ok), "measured": m}; print(("PASS  " if ok else "FAIL  ") + n + (f"  [{m}]" if m else ""))

# ---- kernels: (nu - 1) as functions of y
def nu1_simple(y): return 1.0 / (y * (np.sqrt(1 + 1 / y) + 1))
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
def nu1_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return np.interp(np.log10(y), LYG, HM) / y

def Pl(l, mu): c = np.zeros(l + 1); c[l] = 1; return legval(mu, c)
def dPl(l, mu): c = np.zeros(l + 1); c[l] = 1; return legval(mu, legder(c)) if l > 0 else np.zeros_like(mu)
def menc_frac(r, xi):
    """L340 S1's Gaussian enclosed-mass fraction (heat filter of width xi), with its small-r series."""
    if xi is None: return np.ones_like(r)
    x = r / xi
    f = erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * np.exp(-x**2 / 2)
    return np.where(x < 0.05, math.sqrt(2 / math.pi) * x**3 / 3 * (1 - 0.3 * x**2), f)
def Q2(nu1, a0_si, xi_au=None, ge_si=GE, L=4, Nr=4000, Nmu=256, rmin=1e-2, rmax=3e7):
    """p58's Field.Q2 (copied), with g_sun in the kernel argument replaced by its heat-filtered version."""
    a0 = a0_si * MS2
    if ge_si > 0:
        ye = brentq(lambda y: (1 + float(nu1(np.array(y)))) * y - ge_si / a0_si, 1e-6, 1e3); nue = 1 + float(nu1(np.array(ye)))
    else:
        ye, nue = 0.0, 1.0
    gNe = ye * a0
    r = np.geomspace(rmin, rmax, Nr); mu, wmu = leggauss(Nmu); st = np.sqrt(1 - mu**2)
    R, M = np.meshgrid(r, mu, indexing="ij")
    gsf = -GM * menc_frac(R, xi_au) / R**2
    Gr = gsf + gNe * M; Gt = -gNe * np.sqrt(1 - M**2); Gn = np.sqrt(Gr**2 + Gt**2)
    n1 = nu1(Gn / a0)
    Dr = n1 * Gr - (nue - 1) * gNe * M; Dt = n1 * Gt + (nue - 1) * gNe * np.sqrt(1 - M**2)
    lnr = np.log(r); l = 2
    Drl = (Dr * Pl(l, mu)[None, :]) @ wmu; Dtl = (Dt * (st * dPl(l, mu))[None, :]) @ wmu
    sl = (2 * l + 1) / 2 * (np.gradient(r**2 * Drl, lnr) / r**3 + Dtl / r)
    fout = sl * r**(2 - l)
    Iout0 = float(np.sum(0.5 * (fout[1:] + fout[:-1]) * np.diff(lnr)))
    return -3.0 / 5.0 * Iout0 / YR**2
sig = lambda q: (q - Q2C) / SIG

# ---- unfiltered
a0c = FOOT["canonical"]
q_simple = Q2(nu1_simple, a0c)
print(f"unfiltered simple nu, canonical: Q2 = {q_simple:.4e}  ({sig(q_simple):+.2f} sigma)")
out["unfiltered_simple_canonical"] = q_simple
check("C1 filter off, simple nu, canonical: Q2 = p58's 2.195e-26 to 1%", abs(q_simple / 2.195e-26 - 1) < 0.01, f"{q_simple:.4e}")
qnf = {}
for f, a0 in FOOT.items():
    qnf[f] = Q2(nu1_mono, a0); print(f"unfiltered nu_mono, {f}: Q2 = {qnf[f]:.4e}  ({sig(qnf[f]):+.2f} sigma)")
    out["unfiltered_mono_" + f] = qnf[f]
    if f == "alt": out["unfiltered_simple_alt"] = Q2(nu1_simple, a0)
q0 = Q2(nu1_mono, a0c, xi_au=0.03 * PC_AU, ge_si=0.0)
check("C2 no external field: Q2 ~ 0", abs(q0) < 1e-3 * abs(qnf["canonical"]), f"{q0:.2e}")

# ---- filtered grid
XI = [1e-6, 1e-4, 1e-3, 0.01, 0.030, 0.031, 0.033, 0.045, 0.049, 0.07, 0.10, 0.15, 0.3, 1.0, 3.0]
WIN = (0.030, 0.15)
for f, a0 in FOOT.items():
    rows = []
    rM = math.sqrt(GM / (a0 * MS2))
    print(f"\n{f}: a0 = {a0:.4e}, r_M = {rM:.0f} AU")
    for xi in XI:
        q = Q2(nu1_mono, a0, xi_au=xi * PC_AU)
        rows.append({"xi_pc": xi, "xi_over_rM": xi * PC_AU / rM, "Q2": q, "sigma": sig(q), "in_window": WIN[0] <= xi <= WIN[1]})
        print(f"   xi = {xi:8.1e} pc ({xi*PC_AU/rM:7.3f} r_M): Q2 = {q:+.4e}  ({sig(q):+6.2f} sigma){'  [window]' if WIN[0] <= xi <= WIN[1] else ''}")
    out["rows"][f] = rows
    check(f"C3 {f}: xi = 1e-6 pc equals unfiltered nu_mono to 1%", abs(rows[0]["Q2"] / qnf[f] - 1) < 0.01, f"{rows[0]['Q2']:.4e} vs {qnf[f]:.4e}")
qhi = Q2(nu1_mono, a0c, xi_au=0.03 * PC_AU, Nr=8000, Nmu=512)
qlo = out["rows"]["canonical"][4]["Q2"]
check("C4 grid convergence at the floor (canonical, Nr x2, Nmu x2) < 2%", abs(qhi / qlo - 1) < 0.02, f"{qlo:.4e} -> {qhi:.4e}")


# ---- added after the frozen text (reporting only, disclosed in README): inner-boundary check, 2/3-sigma crossings, field zero
qr = Q2(nu1_mono, a0c, xi_au=0.03 * PC_AU, rmin=1e-3, Nr=5000)
check("C5 (added, informative) inner boundary rmin 1e-2 -> 1e-3 AU at the floor < 1%", abs(qr / qlo - 1) < 0.01, f"{qr:.4e}", )
from scipy.optimize import brentq as _bq
for f, a0 in FOOT.items():
    for k in (2, 3):
        lim = Q2C + k * SIG
        rw = out["rows"][f]; br = [(rw[i - 1]["xi_pc"], rw[i]["xi_pc"]) for i in range(1, len(rw)) if rw[i - 1]["Q2"] > lim >= rw[i]["Q2"]]
        lo_, hi_ = br[-1]   # the last downward crossing on the grid: Q2 <= lim for every larger grid xi
        x = math.exp(_bq(lambda lx: math.log(Q2(nu1_mono, a0, xi_au=math.exp(lx) * PC_AU)) - math.log(lim), math.log(lo_), math.log(hi_), xtol=1e-6))
        out[f"xi_cross_{k}sigma_{f}"] = x; print(f"{f}: Q2 = {lim:.1e} ({k} sigma) at xi = {x:.4f} pc  (passes for xi >= this)")
    gNe = brentq(lambda y: (1 + float(nu1_mono(np.array(y)))) * y - GE / a0, 1e-6, 1e3) * a0
    for xi in (1e-4, 0.03):
        xa = xi * PC_AU * 1.495978707e11; r0 = gNe * xa**3 / (6.674e-11 * 1.98892e30) / 1.495978707e11
        print(f"   {f}: filtered-field zero (small-r estimate g_Ne xi^3/GM) at xi = {xi} pc: r_0 ~ {r0:.3g} AU")

# ---- decision
def ranges(rows, k):
    return [r["xi_pc"] for r in rows if r["in_window"] and abs(r["sigma"]) <= k]
dec = {}
for f in FOOT:
    w = [r for r in out["rows"][f] if r["in_window"]]
    p2 = ranges(out["rows"][f], 2); p3 = ranges(out["rows"][f], 3)
    dec[f] = "ALL" if len(p2) == len(w) else ("NONE" if not p2 else "PART")
    print(f"{f}: window points passing 2 sigma: {p2}; 3 sigma: {p3}; max |sigma| in window = {max(abs(r['sigma']) for r in w):.2f}")
    out[f"pass2_{f}"] = p2; out[f"pass3_{f}"] = p3
V = "SURVIVES" if all(v == "ALL" for v in dec.values()) else ("FAILS" if any(v == "NONE" for v in dec.values()) else "CONDITIONAL")
out["verdict"] = V; print(f"\nVERDICT: kappa = 1/2 {V} CASSINI (window {WIN} pc)")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUT else ""))
json.dump(out, open(os.path.join(HERE, f"cfg357_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if all(res) else 1)
