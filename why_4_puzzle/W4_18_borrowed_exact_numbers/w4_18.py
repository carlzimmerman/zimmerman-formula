#!/usr/bin/env python3
"""W4-18 -- exact numbers borrowed from outside gravity: do any of them fix the 4 (kappa = 1/2)?
Criteria: FROZEN_CRITERIA.md (committed alone, 68d2adb12). Items B1-B9, one declared mapping each.
Light: sympy, mpmath, numpy/scipy (one small Floquet integration); seconds, one core. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_18_borrowed_exact_numbers/w4_18.py > why_4_puzzle/W4_18_borrowed_exact_numbers/w4_18.out
    W4_18_MUTATE=1 ... > .../w4_18_MUTATE.out    (MU1-MU5; exit 1 when every control bites)
kappa = 1/2 FITTED. Not theory closed.
"""
import json, os, re, sys
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("W4_18_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
OUT, checks, items = [], [], {}
W_DATA = (0.227, 0.607)          # CFG493 kappa_Lambda window (CFG894)
S_RHO = 2.99792458e8 * (6.67430e-11 * 0.685 * 8.533238720309458e-27) ** 0.5   # c sqrt(G rho_L), GF1 registers
FOOT = {"canonical": 9.36e-11, "alt": 1.13e-10}


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def pi_parity(expr):
    """pi content of kappa^2: 'pi-free' if kappa^2 has no pi, else the net power of pi it carries."""
    e = sp.simplify(expr ** 2)
    if not e.has(sp.pi):
        return "pi-free"
    num, den = sp.fraction(sp.together(e))
    deg = sp.degree(num, sp.pi) - sp.degree(den, sp.pi)
    return f"pi^{deg} ({'odd' if deg % 2 else 'even'})"


def record(key, cls, kappa=None, note="", members=None):
    d = {"class": cls, "note": note}
    if kappa is not None:
        k = sp.simplify(kappa)
        d.update(kappa_exact=str(k), kappa=float(k), pi=pi_parity(k), in_window=bool(W_DATA[0] <= float(k) <= W_DATA[1]))
    if members:
        d["members"] = {m: dict(kappa_exact=str(sp.simplify(v)), kappa=float(v), pi=pi_parity(v),
                                in_window=bool(W_DATA[0] <= float(v) <= W_DATA[1])) for m, v in members.items()}
    items[key] = d
    kk = f"kappa = {d['kappa_exact']} = {d['kappa']:.4f} [{d['pi']}; in W_data {d['in_window']}]" if kappa is not None else ""
    P(f"  -> {key}: {cls.upper()} {kk} {note}")
    for m, v in (d.get("members") or {}).items():
        P(f"       member {m}: kappa = {v['kappa_exact']} = {v['kappa']:.4f} [{v['pi']}; in W_data {v['in_window']}]")


G, rho, c, M, r, t = sp.symbols("G rho c M r t", positive=True)
H = sp.sqrt(8 * sp.pi * G * rho / 3)
KAP = lambda a0: sp.simplify(a0 / (c * sp.sqrt(G * rho)))
P("W4-18  exact numbers borrowed from outside gravity" + ("  [MUTATE MU1-MU5]" if MUT else ""))
P("theory lane. kappa = 1/2 FITTED. Not theory closed.\n")

# --- COMPUTE START ---
PUMP = 2 if MUT else 1            # MU5: pump H -> 2H
W_EOS = sp.Rational(-9, 10) if MUT else -1    # MU1: w = -0.9
S_SCALE = 2 if MUT else 1         # MU2: Bohlin time scale s -> 2s
TOUCH = 1 if MUT else 2           # MU3: touching d = 2 r_s -> d = r_s
LAM_SIGN = -1 if MUT else 1       # MU4: Lambda -> -Lambda

# B1 parametric resonance: tongue location at eps -> 0 from the exact monodromy trace, then numerical Floquet at eps = 0.02
P("B1 parametric resonance (Mathieu x'' + (delta + eps cos t) x = 0)")
s_ = sp.symbols("s_", positive=True)
roots = sorted(sp.solve(sp.cos(2 * sp.pi * s_) + 1, s_))
ratio = roots[0]                                   # first tongue: mode/pump frequency ratio
P(f"  eps -> 0: |trace| = 2 boundary cos(2 pi sqrt(delta)) = -1 -> first sqrt(delta) = {ratio}; delta = {ratio**2}")


def trace_mono(delta, eps):
    f = lambda tt, y: [y[1], -(delta + eps * np.cos(tt)) * y[0], y[3], -(delta + eps * np.cos(tt)) * y[2]]
    s = solve_ivp(f, (0, 2 * np.pi), [1, 0, 0, 1], rtol=1e-10, atol=1e-12)
    return s.y[0, -1] + s.y[3, -1]


grid = np.arange(0.15, 0.35, 0.001)
unst = [d for d in grid if abs(trace_mono(d, 0.02)) > 2]
tongue = (min(unst), max(unst)) if unst else (np.nan, np.nan)
P(f"  numerical Floquet at eps = 0.02: unstable for delta in [{tongue[0]:.3f}, {tongue[1]:.3f}] (centre {np.mean(tongue):.4f})")
kB1 = KAP(c * ratio * PUMP * H)
record("B1", "odd", kB1, "(a0/c = resonant mode at the pump H's first tongue)")

# B2 Fisher-KPP pulled front
P("\nB2 Fisher-KPP pulled front")
D, rr, k = sp.symbols("D r_g k", positive=True)
v = (D * k ** 2 + rr) / k
kmin = sp.solve(sp.diff(v, k), k)[0]
vstar = sp.simplify(v.subs(k, kmin))
P(f"  v* = min_k (D k^2 + r)/k = {vstar}")
Dsol = sp.solve(sp.Eq(vstar.subs(rr, H), c), D)[0]
width = sp.sqrt(Dsol / H)
kB2 = KAP(c ** 2 / width)
P(f"  secondary reading (v* = c, r = H): D = {sp.simplify(Dsol)}, width = {sp.simplify(width)}, accel c^2/width = {sp.simplify(c**2/width)}")
record("B2", "free", None, "(the vacuum has no transport coefficient D; secondary reading below)")
items["B2"]["secondary"] = dict(kappa_exact=str(sp.simplify(kB2)), kappa=float(kB2), pi=pi_parity(kB2))
P(f"       secondary reading: kappa = {sp.simplify(kB2)} = {float(kB2):.4f} [{pi_parity(kB2)}]")

# B3 Hardy / BF / complementary-series edge
P("\nB3 Hardy / BF / complementary-series edge")
al, ss, l, lam, m = sp.symbols("alpha s l lambda m", real=True)
hardy = sp.solve(sp.discriminant(ss * (ss - 1) + al, ss), al)
P(f"  inverse-square indicial s(s-1) + alpha = 0: double root at alpha = {hardy}")
A = sp.symbols("A", positive=True)
Y = sp.symbols("Y")
radial = sp.diff(r ** 2 * 2 * (A / r) * sp.diff(r ** ss, r), r) / r ** 2           # (1/r^2) d/dr (r^2 . 2|grad Phi0| f')
angular = (A / r) * (-l * (l + 1)) * r ** ss / r ** 2                              # |grad Phi0| grad_perp^2 f
ind = sp.simplify((radial + angular) / (A * r ** (ss - 3)))
expo = sp.solve(ind, ss)
P(f"  deep-MOND point-mass perturbation operator, f = r^s Y_lm: indicial {sp.factor(ind)} = 0 -> s = {expo}")
P(f"  double root only where l(l+1) = 0 (the log monopole); no tunable inverse-square coupling -> no Hardy slot")
edge = sp.solve(sp.discriminant(lam ** 2 + 3 * lam + m ** 2, lam), m)
edge = [e for e in edge if e.is_positive][0]
P(f"  dS4 scalar exponents lambda^2 + 3 lambda + m^2/H^2 = 0: critical damping / complementary-series edge m = {edge} H")
record("B3", "odd", KAP(c * edge * H), "(edge reading a0/c = m_edge; Hardy reading has no slot)")

# B4 Thomson / Eddington pi cancellation
P("\nB4 Thomson / Eddington pi cancellation")
mp_, re_ = sp.symbols("m_p r_e", positive=True)
LEdd = sp.simplify(4 * sp.pi * G * M * mp_ * c / (sp.Rational(8, 3) * sp.pi * re_ ** 2))
P(f"  L_Edd = 4 pi G M m_p c / sigma_T, sigma_T = (8 pi/3) r_e^2 -> {LEdd}  (pi-free: {not LEdd.has(sp.pi)})")
transfer = sp.simplify(rho * (1 + W_EOS))
P(f"  momentum transfer of the source to matter ~ (rho + p/c^2) = rho (1 + w) = {transfer} at w = {W_EOS}")
record("B4", "nk" if transfer == 0 else "free", None, "(VOID: a Lorentz-invariant vacuum transfers no momentum)" if transfer == 0
       else "(transfer nonzero; a balance needs a free cross-section)")

# B5 Newton-Hooke duality
P("\nB5 Newton-Hooke duality (Bohlin map w = z^2, d tau/dt = s|z|^2)")
h, om, sc_, kk, Z2 = sp.symbols("h omega s k Z2", positive=True)       # Z2 stands for |z|^2
EK = (4 / (sc_ ** 2 * Z2)) * (2 * h - om ** 2 * Z2) / 2 - kk / Z2
ksol = sp.solve(sp.Eq(sp.expand(EK * Z2).coeff(Z2, 0), 0), kk)[0]
EKc = sp.simplify(EK.subs(kk, ksol))
P(f"  Kepler energy constant iff k = {ksol}; then E_K = {EKc}  (k depends on the free time scale s -> amplitude not fixed)")
kdual = ksol.subs(sc_, S_SCALE)
Aexp = lambda a: sp.Rational(4, a + 3) - 3
P(f"  dual exponents (a+3)(A+3) = 4: Hooke a = 1 -> A = {Aexp(1)}; deep MOND a = -1 -> A = {Aexp(-1)} (self-dual)")
aa, bb = 2.0, 1.0
tt = np.linspace(0, 2 * np.pi, 721)
w = (aa * np.cos(tt) + 1j * bb * np.sin(tt)) ** 2
cen, sa, sb = (aa ** 2 - bb ** 2) / 2, (aa ** 2 + bb ** 2) / 2, aa * bb
ell = np.max(np.abs(((w.real - cen) / sa) ** 2 + (w.imag / sb) ** 2 - 1))
focus = cen - np.sqrt(sa ** 2 - sb ** 2)
record("B5", "nk", None, "(EXPONENT-ONLY)")

# B6 mean-field and critical-damping ratios
P("\nB6 mean-field and critical-damping ratios")
a_, b_, tm = sp.symbols("a b t_m", positive=True)
phi = sp.symbols("phi", real=True)
F = -a_ * tm * phi ** 2 + b_ * phi ** 4                  # below T_c (reduced temperature -t_m)
phi0 = sp.solve(sp.diff(F, phi), phi)
phi0 = [p for p in phi0 if p.is_positive][0]
chi_below = 1 / sp.diff(F, phi, 2).subs(phi, phi0)
chi_above = 1 / sp.diff(a_ * tm * phi ** 2 + b_ * phi ** 4, phi, 2).subs(phi, 0)
gam = sp.solve(sp.discriminant(lam ** 2 + sp.Symbol("gamma") * lam + om ** 2, lam), sp.Symbol("gamma"))
P(f"  Landau chi_above/chi_below at equal |t| = {sp.simplify(chi_above / chi_below)}; critical damping gamma = {[g for g in gam if g.is_positive]}")
record("B6", "nk", None, "(NO SLOT: no order parameter shared by a0 and rho_Lambda; damping reading = B3 edge)")

# B7 lattices of touching horizons
P("\nB7 lattices of touching horizons (brief X5, light part)")
mm, dd = sp.symbols("m d", positive=True)
lat = {"sc": ([(1, 0, 0), (0, 1, 0), (0, 0, 1)], 1, 1),
       "bcc": ([(1, 1, -1), (-1, 1, 1), (1, -1, 1)], 1, sp.sqrt(3)),
       "fcc": ([(1, 1, 0), (0, 1, 1), (1, 0, 1)], 1, sp.sqrt(2)),
       "hcp": ([(2, 0, 0), (1, sp.sqrt(3), 0), (0, 0, 2 * sp.sqrt(sp.Rational(8, 3)))], 2, 2)}
vs = {}
for nm, (vecs, nat, dnn) in lat.items():
    vol = abs(sp.Matrix(vecs).det()) / nat
    vs[nm] = sp.nsimplify(sp.simplify(vol / dnn ** 3))
    P(f"  {nm}: volume per site / d^3 = {vs[nm]} = {float(vs[nm]):.4f}")
rs = 2 * G * mm / c ** 2
dtouch = TOUCH * rs
comp = sp.simplify(G * mm / (dtouch * c ** 2))
P(f"  touching: d = {TOUCH} r_s = {sp.simplify(dtouch)} -> compactness G m/(d c^2) = {comp}")
ident = sp.simplify((G * mm / dd ** 2) ** 2 - G * (mm / (vs['sc'] * dd ** 3)) * c ** 2 * vs['sc'] * (G * mm / (dd * c ** 2)))
memb = {nm: sp.sqrt(vs[nm] * comp) for nm in ("sc", "bcc", "fcc", "hcp")}
record("B7", "menu", None, "(dust lattice, w = 0; P-cube = sc, P-dense = fcc/hcp)", members=memb)

# B8 Lambda thresholds x MOND (static part)
P("\nB8 Lambda thresholds x MOND (units a0 = 1, H = 1; mu_M = G M H^4/a0^3)")
mp.mp.dps = 30
NU = {"Newton": lambda y: 1,
      "deep MOND": lambda y: 1 / mp.sqrt(y),
      "simple": lambda y: (1 + mp.sqrt(1 + 4 / y)) / 2,
      "standard": lambda y: mp.sqrt((1 + mp.sqrt(1 + 4 / y ** 2)) / 2),
      "RAR": lambda y: 1 / (1 - mp.exp(-mp.sqrt(y)))}
L2 = LAM_SIGN


def thresholds(law, muM):
    g = lambda x: (muM / x ** 2) * NU[law](muM / x ** 2)
    zf = lambda x: g(x) - L2 * x
    osco = lambda x: mp.diff(lambda y: y ** 3 * g(y), x) - 4 * L2 * x ** 3
    out = {}
    for nm, f in (("zero-force", zf), ("OSCO", osco)):
        xs = [mp.mpf(10) ** e for e in np.arange(-12, 12.01, 0.05)]
        root = None
        for x0, x1 in zip(xs[:-1], xs[1:]):
            if f(x0) * f(x1) < 0:
                root = mp.findroot(f, (x0, x1), solver="bisect"); break
        out[nm] = None if root is None else dict(r=root, g=g(root), rho_ratio=2 * muM / root ** 3)
    return out


b8 = {}
for law in NU:
    b8[law] = {}
    for thr in ("zero-force", "OSCO"):
        row = []
        for e in (-8, -6, 6, 8):
            res = thresholds(law, mp.mpf(10) ** e)[thr]
            row.append(None if res is None else (e, res["g"], res["rho_ratio"]))
        if any(x is None for x in row):
            b8[law][thr] = None
            P(f"  {law:10s} {thr:10s}: no root")
            continue
        sl = lambda i, j, q: float(mp.log10(row[j][q] / row[i][q]) / (row[j][0] - row[i][0]))
        b8[law][thr] = dict(g_slope_smallM=sl(0, 1, 1), g_slope_largeM=sl(2, 3, 1), rho_slope_smallM=sl(0, 1, 2),
                            rho_slope_largeM=sl(2, 3, 2), rho_ratio_largeM=float(row[3][2]), rho_ratio_smallM=float(row[0][2]))
        q = b8[law][thr]
        P(f"  {law:10s} {thr:10s}: d log g/d log M = {q['g_slope_smallM']:+.4f} (small M), {q['g_slope_largeM']:+.4f} (large M); "
          f"rho_bar/rho_L slope {q['rho_slope_smallM']:+.4f} / {q['rho_slope_largeM']:+.4f}; rho_bar/rho_L at large M {q['rho_ratio_largeM']:.4f}")
flat = [(law, thr) for law in b8 for thr in b8[law] if b8[law][thr] and
        (abs(b8[law][thr]["g_slope_smallM"]) < 1e-3 or abs(b8[law][thr]["g_slope_largeM"]) < 1e-3)]
P(f"  M-independent threshold accelerations: {flat or 'none'}; and none can carry c (static Newton/MOND + Lambda has no c)")
record("B8", "nk", None, "(no M-independent acceleration; without c none could fix kappa = a0/(c sqrt(G rho)))")

# B9 Maxwellian sqrt(pi)
P("\nB9 Maxwellian sqrt(pi)")
vv, sg, th = sp.symbols("v sigma theta", positive=True)
fmb = (2 * sp.pi * sg ** 2) ** sp.Rational(-3, 2) * sp.exp(-vv ** 2 / (2 * sg ** 2))
vbar = sp.simplify(sp.integrate(4 * sp.pi * vv ** 3 * fmb, (vv, 0, sp.oo)))
hemi = sp.simplify(sp.integrate(sp.cos(th) * sp.sin(th), (th, 0, sp.pi / 2)) * 2 * sp.pi / (4 * sp.pi))
P(f"  mean speed = {vbar} (carries an inverse square root of pi relative to sigma); effusion flux = {hemi} n v_bar")
record("B9", "nk", None, "(VOID: the w = -1 source has no velocity distribution)")
# --- COMPUTE END ---

P("\nChecks")
if not MUT:
    Zs = sp.sqrt(32 * sp.pi / 3)
    check("K1 Friedmann identity kappa^2 = 8 pi/(3 Z^2) at Z^2 = 32 pi/3", sp.simplify(8 * sp.pi / (3 * Zs ** 2)),
          sp.simplify(8 * sp.pi / (3 * Zs ** 2)) == sp.Rational(1, 4))
    nz, no = b8["Newton"]["zero-force"]["rho_ratio_largeM"], b8["Newton"]["OSCO"]["rho_ratio_largeM"]
    check("K2 Newton zero-force 2 rho_L, OSCO 8 rho_L", f"{nz:.10f}, {no:.10f}", abs(nz - 2) < 1e-9 and abs(no - 8) < 1e-9)
    check("K3 volume per site / d^3 = 1, 4/(3 sqrt3), 1/sqrt2, 1/sqrt2", [str(vs[x]) for x in vs],
          [sp.simplify(vs[x] - y) for x, y in (("sc", 1), ("bcc", 4 / (3 * sp.sqrt(3))), ("fcc", 1 / sp.sqrt(2)), ("hcp", 1 / sp.sqrt(2)))] == [0] * 4)
    check("K4 Mathieu first tongue at eps = 0.02 within 0.02 of 1/4", f"[{tongue[0]:.3f}, {tongue[1]:.3f}]",
          abs(tongue[0] - 0.25) < 0.02 and abs(tongue[1] - 0.25) < 0.02)
    check("K5 KPP minimum speed = 2 sqrt(D r)", vstar, sp.simplify(vstar - 2 * sp.sqrt(D * rr)) == 0)
    check("K6 Bohlin: Hooke ellipse -> Kepler ellipse with focus at origin; exponents", f"ellipse residual {ell:.1e}, focus {focus:.1e}, A(1) {Aexp(1)}, A(-1) {Aexp(-1)}",
          ell < 1e-6 and abs(focus) < 1e-6 and Aexp(1) == -2 and Aexp(-1) == -1)
    check("K7 lattice identity a_nn^2 = G rho c^2 (V_s/d^3)(G m/(d c^2))", ident, ident == 0)
    src = open(os.path.abspath(__file__)).read()
    blk = src.split("# --- COMPUTE START ---")[1].split("# --- COMPUTE END ---")[0]
    bad = [p for p in (r"(?<![\d.])0\.5(?!\d)", r"(?<![\w.)])1\s*/\s*2(?!\d)", r"(?<![\d.])0\.25(?!\d)", r"(?<![\w.)])1\s*/\s*4(?!\d)",
                       r"Rational\(\s*1\s*,\s*[24]\s*\)", r"S\.Half") if re.search(p, blk)]
    check("I1 forbidden-token scan of the compute block", bad or "clean", not bad)

sel = [kx for kx, d in items.items() if d.get("class") != "menu" and d.get("kappa_exact") == "1/2"]
menu_half = [m for m, d in items["B7"]["members"].items() if d["kappa_exact"] == "1/2"]
lane = ("AN OUTSIDE NUMBER FIXES THE 4" if sel else "MENU ONLY" if menu_half else "NO OUTSIDE NUMBER FIXES THE 4")
P(f"\nSELECTS: {sel or 'none'};  pi-free menu members equal to 1/2: {menu_half or 'none'} (B7, two declared principles disagree)")
for f, a0 in FOOT.items():
    P(f"  footing {f}: measured kappa_Lambda = a0/(c sqrt(G rho_L)) = {a0 / S_RHO:.3f}")
P(f"LANE VERDICT: {lane}")
json.dump(dict(mutate=MUT, items=items, b8=b8, tongue=list(map(float, tongue)), lane_verdict=lane, checks=checks),
          open(os.path.join(HERE, f"w4_18_results{SUF}.json"), "w"), indent=1, default=str)
if MUT:
    try:
        base = json.load(open(os.path.join(HERE, "w4_18_results.json")))
        bi = base["items"]
        mu = {"MU1 B4 no longer VOID": items["B4"]["class"] != bi["B4"]["class"],
              "MU2 B5 dual coupling changes": sp.simplify(kdual - ksol.subs(sc_, 1)) != 0,
              "MU3 B7 sc moves off its base value": abs(items["B7"]["members"]["sc"]["kappa"] - bi["B7"]["members"]["sc"]["kappa"]) > 1e-9,
              "MU4 B8 thresholds vanish": all(b8[law][thr] is None for law in b8 for thr in b8[law]),
              "MU5 B1 kappa doubles": abs(items["B1"]["kappa"] / bi["B1"]["kappa"] - 2) < 1e-9}
        for kx, ok in mu.items():
            P(f"MUTATE {kx}: {ok}")
        sys.exit(1 if all(mu.values()) else 2)
    except OSError:
        sys.exit(2)
P(f"\nchecks: {sum(x['pass'] for x in checks)}/{len(checks)} pass")
sys.exit(0 if all(x["pass"] for x in checks) else 1)
