#!/usr/bin/env python3
"""CQB1: does CQ2's sealed Gaia DR4 wide-binary prediction hold with the adopted Pi^6 blend as the stiffness?
Criteria: FROZEN_CRITERIA.md (37f878538f), committed alone before this script.
Run from anywhere:  OMP_NUM_THREADS=1 nice -n 10 python3 -I -B cqb1.py [--mutate M1|M1b|M2|M3]
Needs the KA1 reproduction first (the byte-identical copy ./cq2.py, run once, writes ./cq2.json).
Reads only: CQ2's folder, X3's json and script, AC21 iter_6 form.json, QX19's script, CQ2's criteria (text pins).
kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import hashlib, json, math, sys, time
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy.integrate import quad, simpson

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CQ2D = os.path.join(REPO, "cq_lanes_2026_11_04", "CQ2_v3s_dr4_seal")
X3D = os.path.join(REPO, "rebuild_2026_10_22", "X3_switched_stiffness")
FORMJ = os.path.join(REPO, "action_search_2026_11_05", "AC21_smooth_3d", "iter_6_fast_decay", "form.json")
QX19PY = os.path.join(REPO, "closure_2026_11_06", "QX19_one_action_scorecard", "qx19.py")

MUT = None
if "--mutate" in sys.argv:
    MUT = sys.argv[sys.argv.index("--mutate") + 1]
    assert MUT in ("M1", "M1b", "M2", "M3"), MUT
SFX = f"_MUTATE_{MUT}" if MUT else ""
OUT, RES, CHK = [], {"lane": "CQB1_cq2_under_blend", "criteria": "37f878538f", "mutate": MUT}, {}
HDR = "kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework."


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, msg):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), msg=msg)
    P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


P(f"CQB1 (criteria 37f878538f){'  [MUTATE ' + MUT + ']' if MUT else ''}")
P(HDR)
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5

# ---------------------------------------------------------------- this lane's own SI constants (U1-U4)
G_SI = 6.67430e-11                       # CODATA 2018
C_SI = 299792458.0                        # exact
AU_SI = 149597870700.0                    # IAU 2012, exact
PC_SI = 648000.0 / math.pi * AU_SI        # IAU 2015, exact
MSUN_SI = 1.3271244e20 / G_SI             # IAU 2015 nominal GM_sun over G
MSUN_PC3_SI = MSUN_SI / PC_SI ** 3        # kg/m^3 per Msun/pc^3
KPC_SI = 1e3 * PC_SI

# ================================================================ K0: inputs pinned
P("\n== K0: inputs pinned (sha256)")
pins = {os.path.join(CQ2D, "cq2.py"): "6fbf2abfe5e06d0b7e09a6dc31f907afd0f3e86eceb40f936ed24f69a13a9b5c",
        os.path.join(CQ2D, "cq2.json"): "a73f754ced4fd4af67fe34963780550f9f5bd8fe8551965a3ca15971c4cae61c",
        FORMJ: "77a58d28fbaae45ca297003af46fb06d93dc86057373367b9a81735f6a0a40a2",
        os.path.join(X3D, "x3_switched_stiffness_results.json"): "8d63aac13dbadcd3c2279cf93ad3db33ed3c1380b71b380086bcd72ee5f36175"}
k0 = {os.path.relpath(p, REPO): (sha(p) == h) for p, h in pins.items()}
for k_, v_ in k0.items():
    P(f"  {k_}: {'matches' if v_ else 'DIFFERS'}")
check("K0", all(k0.values()), "CQ2's cq2.py / cq2.json, AC21 form.json and X3's json match their pinned sha256")
CQ2J = json.load(open(os.path.join(CQ2D, "cq2.json")))

# ================================================================ KA1: CQ2 reproduced by its byte-identical copy
P("\n== KA1: CQ2's cq2.py, byte-identical copy run from this folder (outputs here, never in CQ2's folder)")
copy_ok = sha(os.path.join(HERE, "cq2.py")) == pins[os.path.join(CQ2D, "cq2.py")]
REP = json.load(open(os.path.join(HERE, "cq2.json")))


def leaves(x, path=""):
    if isinstance(x, dict):
        for k_, v_ in x.items():
            yield from leaves(v_, f"{path}/{k_}")
    elif isinstance(x, list):
        for i_, v_ in enumerate(x):
            yield from leaves(v_, f"{path}[{i_}]")
    elif isinstance(x, bool) or x is None or isinstance(x, str):
        yield path, x
    else:
        yield path, float(x)


def rel(a, b):
    return 0.0 if a == b else abs(a - b) / max(abs(a), abs(b), 1e-300)


L1, L2 = dict(leaves(CQ2J)), dict(leaves(REP))
skip = ("/wall_s", "/peak_rss_gb")
num_keys = [k_ for k_, v_ in L1.items() if isinstance(v_, float) and k_ not in skip]
missing = [k_ for k_ in L1 if k_ not in L2 and k_ not in skip]
all_rel = max(rel(L1[k_], L2[k_]) for k_ in num_keys if k_ in L2)
other_diff = [k_ for k_, v_ in L1.items() if not isinstance(v_, float) and k_ not in skip and L2.get(k_) != v_]
named = {}
named["switch.min_binary_margin"] = rel(CQ2J["switch"]["min_binary_margin"], REP["switch"]["min_binary_margin"])
named["switch.near_zone_min"] = rel(CQ2J["switch"]["near_zone_min"], REP["switch"]["near_zone_min"])
for f in FOOTS:
    a_, b_ = CQ2J["gamma_r"][f"{f}|1.9e-10|M1.0"]["gamma_r_minus_1"], REP["gamma_r"][f"{f}|1.9e-10|M1.0"]["gamma_r_minus_1"]
    named[f"gamma_r grid {f}"] = max(rel(x, y) for x, y in zip(a_, b_))
    named[f"DR3 {f}"] = max(rel(L1[k_], L2[k_]) for k_ in num_keys if k_.startswith(f"/DR3/{f}"))
named["pipeline gamma_inf (all)"] = max(rel(L1[k_], L2[k_]) for k_ in num_keys if k_.startswith("/pipeline/out"))
rep_checks = {k_: v_["ok"] for k_, v_ in REP["checks"].items()}
for k_, v_ in named.items():
    P(f"  {k_}: max rel {v_:.1e}")
P(f"  every numeric leaf of cq2.json ({len(num_keys)} leaves, wall time and RSS excluded): max rel {all_rel:.1e}; "
  f"missing {len(missing)}; non-numeric differences {len(other_diff)}")
P(f"  reproduction's own checks: {rep_checks}; its verdict {REP['verdict']}")
P(f"  sealed values reproduced: switch margin {REP['switch']['min_binary_margin']:.4g}, near zone "
  f"{REP['switch']['near_zone_min']:+.4f} Msun/pc^3, gamma_r - 1 at 30 kAU canonical "
  f"{REP['gamma_r']['canonical|1.9e-10|M1.0']['gamma_r_minus_1'][-1]:.4e}, alt {REP['gamma_r']['alt|1.9e-10|M1.0']['gamma_r_minus_1'][-1]:.4e}")
RES["KA1"] = dict(copy_sha_ok=copy_ok, named_max_rel=named, all_leaves_max_rel=all_rel, n_leaves=len(num_keys),
                  missing=missing, non_numeric_diff=other_diff, repro_checks=rep_checks, repro_verdict=REP["verdict"])
check("KA1", copy_ok and max(named.values()) <= 1e-9 and all(rep_checks.values()) and not missing,
      f"byte-identical copy; named numbers max rel {max(named.values()):.1e} (line 1e-9); all leaves {all_rel:.1e}; "
      f"reproduction's K1-K7 all PASS: {all(rep_checks.values())}")

# ================================================================ KA2: this lane's Route F copy (copied from cq2.py)
# CQ2's constants, so the known answer is the same computation (r/L* uses CQ2's AU and PC)
G, MS, AU, PC = 6.6743e-11, 1.98892e30, 1.495978707e11, 3.0857e16
LFL = {"canonical": 21.682, "alt": 22.849}
S_KAU = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30], float)
GPRI = 1.9e-10


def chi_c6(kap, c, xe):
    m = (1 - c * c) / (1 + xe) + c * c / (1 + xe) ** 2
    return m / (1 - m + kap ** 2 * m / 2)


def routeF_radial(GM, L, xe, r, nc=48, kmul=400.0, nk=200000):
    """Monopole anomalous radial acceleration at r of a point mass GM in a uniform Galactic field x_e = g/a0 (screened, L*)."""
    rho = r / L
    cg, cw = np.polynomial.legendre.leggauss(nc)
    K = kmul / rho
    lk = np.linspace(np.log(1e-6), np.log(K), nk); k = np.exp(lk)
    c0 = np.concatenate([0.5 * (chi_c6(kk[:, None], cg[None, :], xe) * cw).sum(1) for kk in np.array_split(k, 20)])
    z = k * rho
    j1 = np.where(z < 1e-3, z / 3 - z ** 3 / 30, np.sin(z) / z ** 2 - np.cos(z) / z)
    head = np.trapz(k * k * j1 * c0, lk)
    a = K * rho
    t1 = quad(lambda zz: 1 / zz ** 3, a, np.inf, weight="sin", wvar=1.0)[0]
    t2 = quad(lambda zz: 1 / zz ** 2, a, np.inf, weight="cos", wvar=1.0)[0]
    return 2 * GM / (np.pi * L ** 2) * (head + 2 * (t1 - t2))


P("\n== KA2: this lane's Route F copy vs CQ2's json (1 Msun, primary field, L* floor; s = 1, 10, 30 kAU)"
  + ("  [M2: the two footings' L* floors SWAPPED]" if MUT == "M2" else ""))
lfl_use = {"canonical": LFL["alt"], "alt": LFL["canonical"]} if MUT == "M2" else dict(LFL)
ka2 = {}
for f in FOOTS:
    L = lfl_use[f] * PC; xe = GPRI / A0[f]; ref = CQ2J["gamma_r"][f"{f}|1.9e-10|M1.0"]["gamma_r_minus_1"]
    vals = []
    for j in (0, 5, 8):
        r = S_KAU[j] * 1e3 * AU
        g1 = routeF_radial(G * MS, L, xe, r) / (G * MS / r ** 2)
        vals.append((S_KAU[j], g1, ref[j], rel(g1, ref[j])))
    ka2[f] = vals
    P(f"  [{f}] " + "; ".join(f"s {s:g} kAU: {g1:.6e} (CQ2 {rf:.6e}, rel {e:.1e})" for s, g1, rf, e in vals))
ka2max = max(v[3] for vs in ka2.values() for v in vs)
RES["KA2"] = {f: [dict(s_kAU=v[0], mine=v[1], cq2=v[2], rel=v[3]) for v in vs] for f, vs in ka2.items()}
check("KA2", ka2max <= 1e-9, f"max rel {ka2max:.1e} (line 1e-9)")

# ================================================================ U1-U3: Sigma and b, same quantity, same units
P("\n== U1: rho_DE from the a0 law, SI, this lane's constants (a0 = kappa c sqrt(G rho_DE), kappa = 1/2)"
  + ("  [M3: 1/kappa^2 DROPPED]" if MUT == "M3" else ""))
RHO_DE_SI, RHO_DE = {}, {}
for f in FOOTS:
    kfac = 1.0 if MUT == "M3" else KAPPA ** 2
    RHO_DE_SI[f] = A0[f] ** 2 / (kfac * C_SI ** 2 * G_SI)
    RHO_DE[f] = RHO_DE_SI[f] / MSUN_PC3_SI
    back = KAPPA * C_SI * math.sqrt(G_SI * RHO_DE_SI[f])
    P(f"  [{f}] a0 {A0[f]:.5g} m/s^2 -> rho_DE {RHO_DE_SI[f]:.5e} kg/m^3 = {RHO_DE[f]:.5e} Msun/pc^3 "
      f"(1 Msun/pc^3 = {MSUN_PC3_SI:.6e} kg/m^3); a0 back from rho_DE {back:.5g}")
RES["U1"] = dict(rho_DE_kg_m3=RHO_DE_SI, rho_DE_Msun_pc3=RHO_DE, Msun_pc3_kg_m3=MSUN_PC3_SI)
check("U1", all(RHO_DE[f] > 0 for f in FOOTS), "rho_DE computed in SI on both footings")

P("\n== U2: the b the blend's own lanes use (QX19: G = c = 1, K = 4 pi, s2v = 8 ag^2, b = s2v/2) vs G rho_DE / c^2")
qx19src = open(QX19PY).read()
pin_b = "ag = A0 / cl ** 2; Kn = 4 * math.pi; s2v = 8 * ag ** 2; bv = s2v / 2" in qx19src
u2 = {}
for f in FOOTS:
    ag = A0[f] / C_SI ** 2; bv = (8 * ag ** 2) / 2          # m^-2, QX19's expression
    bg = G_SI * RHO_DE_SI[f] / C_SI ** 2                    # m^-2, from U1
    u2[f] = dict(qx19_b_m2=bv, G_rhoDE_over_c2_m2=bg, rel=rel(bv, bg))
    P(f"  [{f}] QX19 b = {bv:.6e} m^-2; G rho_DE / c^2 = {bg:.6e} m^-2; rel {u2[f]['rel']:.1e}")
P(f"  QX19's line for b found verbatim in qx19.py: {pin_b}")
RES["U2"] = u2
check("U2", pin_b and max(v["rel"] for v in u2.values()) <= 1e-12,
      f"b (QX19, geometric) = G rho_DE / c^2: max rel {max(v['rel'] for v in u2.values()):.1e} (line 1e-12)")

P("\n== U3: Sigma's normalisation (D.P in the action vs the D.P X3 and CQ2 report in Msun/pc^3)")
x3src = open(os.path.join(X3D, "x3_switched_stiffness.py")).read()
cq2crit = open(os.path.join(CQ2D, "FROZEN_CRITERIA.md")).read()
pins3 = {
    "CQ2 criteria: (L) lap Phi = K rho + div p, p = K P": ("(L) ∇²Φ = Kρ + ∇·p" in cq2crit and "p = K P" in cq2crit),
    "QX19: P = p / K, K = 4 pi (G = c = 1)": ("Pm = ag / Kn" in qx19src and "Kn = 4 * math.pi" in qx19src
                                               and "Geometric units G = c = 1, K = 4 pi" in qx19src),
    "X3 lobes: D.P = div p_SI / (4 pi G) / (Msun/pc^3)": ("Dsun = sv.divfield() * A0[foot] / a_s / (4 * math.pi * G_SI) / MSUN_PC3" in x3src),
    "X3 Galactic phantom: mass density / (Msun/pc^3)": ("rho = lv[\"rho\"] * Md * MSUN / L ** 3 / MSUN_PC3" in x3src),
    "X3: MSUN_PC3 = MSUN / PC ** 3": ("MSUN_PC3 = MSUN / PC ** 3" in x3src),
}
for k_, v_ in pins3.items():
    P(f"  text pin, {k_}: {'found' if v_ else 'NOT FOUND'}")
x3_msun = float(x3src.split("\nMSUN = ")[1].split("\n")[0]); x3_pc = float(x3src.split("\nPC = ")[1].split("\n")[0])
x3_mpc3 = x3_msun / x3_pc ** 3
u3rel = rel(x3_mpc3, MSUN_PC3_SI)
P(f"  X3's Msun/pc^3 = {x3_mpc3:.6e} kg/m^3 (MSUN {x3_msun:.6g}, PC {x3_pc:.10g}); this lane's {MSUN_PC3_SI:.6e}; rel {u3rel:.1e}")
P("  Derivation (static weak field, G = c = 1): (L) lap Phi = 4 pi rho + div p with p = K P, K = 4 pi, so div p = 4 pi rho_ph(geom)")
P("  and Sigma = D.P = div P = div p / K = rho_ph(geom) = G rho_ph / c^2, rho_ph = div p_SI / (4 pi G).")
P("  b = rho_DE(geom) = G rho_DE / c^2 (U2). Hence Sigma / b = rho_ph / rho_DE, both in Msun/pc^3: the same quantity, same units.")
P("  Cross-reference (not a gate): TC1 N2 reads 'Sigma/X = 2 + rho_ph/rho_DE' for AC2q (Sigma = D.P + 2X, X = rho_DE scale).")
RES["U3"] = dict(text_pins=pins3, x3_Msun_pc3=x3_mpc3, lane_Msun_pc3=MSUN_PC3_SI, rel=u3rel)
check("U3", all(pins3.values()) and u3rel <= 1e-3,
      f"unit chain pinned in the record's text; X3's Msun/pc^3 vs this lane's rel {u3rel:.1e} (line 1e-3)")

# ================================================================ S1: the blend, exact, from form.json
P("\n== S1: the blend f from AC21 iter_6 form.json, exact (sympy)")
form = json.load(open(FORMJ))
q, t, Sg, bb = sp.symbols("q t Sigma b", positive=True)
pieces = [(sp.Rational(lo), sp.Rational(hi), sp.sympify(e, locals={"q": q})) for lo, hi, e in form["pieces"]]
fp_lo, f_lo = sp.Integer(0), sp.Integer(0)
SH = []   # per piece: lo, hi, (f'', f', f) as polynomials in t = q - lo
knot_c = []
prev = None
for lo, hi, e in pieces:
    fpp_t = sp.expand(e.subs(q, lo + t))
    fp_t = sp.expand(fp_lo + sp.integrate(fpp_t, t))
    f_t = sp.expand(f_lo + sp.integrate(fp_t, t))
    if prev is not None:   # continuity of f'' and its first two derivatives at the knot (C4 overall)
        pe, plo, phi_ = prev
        knot_c.append(all(sp.simplify(sp.diff(pe, q, k_).subs(q, lo) - sp.diff(e, q, k_).subs(q, lo)) == 0 for k_ in range(3)))
    prev = (e, lo, hi)
    SH.append((lo, hi, fpp_t, fp_t, f_t))
    fp_lo, f_lo = fp_t.subs(t, hi - lo), f_t.subs(t, hi - lo)
lo_l, hi_l, fpp_last, _, _ = SH[-1]
f1, fp1, fpp1 = sp.nsimplify(f_lo), sp.nsimplify(fp_lo), sp.simplify(fpp_last.subs(t, hi_l - lo_l))
# derivatives of f'' at q = 1 from the left vs the constant 1 above (C4 at q = 1 needs f''' = f'''' = 0 there)
d1_1 = sp.simplify(sp.diff(pieces[-1][2], q).subs(q, 1)); d2_1 = sp.simplify(sp.diff(pieces[-1][2], q, 2).subs(q, 1))
A6 = sp.simplify(SH[0][4].coeff(t, 6))
P(f"  f(1) = {f1}, f'(1) = {fp1}, f''(1-) = {fpp1}, f'''(1-) = {d1_1}, f''''(1-) = {d2_1}; f = {A6} q^6 on (0, 1/2]"
  f" (QX19 C6 states 122363904/44610575: {A6 == sp.Rational(122363904, 44610575)}); interior knots C4: {knot_c}")
# above q = 1: f'' = 1, so f = f(1) + f'(1)(q-1) + (q-1)^2/2
f_hi = f1 + fp1 * (q - 1) + (q - 1) ** 2 / 2
ok_hi = sp.simplify(f_hi - q ** 2 / 2) == 0
Fb = bb ** 2 * (Sg / bb) ** 2 / 2         # F = b^2 f(Sigma/b) on Sigma >= b with f = q^2/2 there
Fp, Fpp, dFb = sp.diff(Fb, Sg), sp.diff(Fb, Sg, 2), sp.diff(Fb, bb)
ok_F = (sp.simplify(Fb - Sg ** 2 / 2) == 0 and sp.simplify(Fp - Sg) == 0 and sp.simplify(Fpp - 1) == 0
        and sp.simplify(dFb) == 0 and sp.simplify(Sg * Fp - 2 * Fb) == 0)
P(f"  q >= 1: f = q^2/2 exactly: {ok_hi}; Sigma >= b: F = Sigma^2/2, F' = Sigma, F'' = 1, dF/db = 0, Sigma F' = 2F: {ok_F}")
P("  q <= 0: f = 0 by the form's definition (f(0) = f'(0) = 0 and f = A q^6 near 0, so the join at 0 is C5)")

# stable float evaluators: shifted polynomials (Horner in t = q - lo)
EV = []
for lo, hi, fpp_t, fp_t, f_t in SH:
    cs = [np.array([float(c) for c in sp.Poly(x, t).all_coeffs()]) for x in (fpp_t, fp_t, f_t)]
    EV.append((float(lo), float(hi), cs))


def fblend(qv, which):
    """which: 0 -> f'', 1 -> f', 2 -> f. Vectorised."""
    qv = np.asarray(qv, float); out = np.zeros_like(qv)
    hi1 = qv >= 1.0
    out[hi1] = (1.0, qv[hi1], qv[hi1] ** 2 / 2)[which] if which else 1.0
    for lo, hi, cs in EV:
        sel = (qv > lo) & (qv <= hi) & ~hi1
        if sel.any():
            out[sel] = np.polyval(cs[which], qv[sel] - lo)
    return out


qq = np.linspace(0.0, 1.0, 200001)
fpp_d = fblend(qq, 0)
fpp_max, q_at_max = float(fpp_d.max()), float(qq[np.argmax(fpp_d)])
fpp_min_layer = float(fpp_d[qq >= 0.5].min())
q_unit = float(sp.Rational(form["A"]) ** sp.Rational(-1, 4))     # A q^4 = 1 on (0, 1/2]
fp_d = fblend(qq, 1)
mono = bool(np.all(np.diff(fp_d) > 0))
fe = float(abs(fblend(np.array([1.0 - 1e-12]), 2)[0] - 0.5)), float(abs(fblend(np.array([1.0 - 1e-12]), 1)[0] - 1.0))
P(f"  f'' on [0, 1]: max {fpp_max:.4f} at q {q_at_max:.4f}; min on [1/2, 1] {fpp_min_layer:.4f}; f'' = 1 below 1/2 at "
  f"q = A^(-1/4) = {q_unit:.4f}; f' strictly increasing on (0, 1]: {mono}; float evaluator at q = 1-: |f - 1/2| {fe[0]:.1e}, "
  f"|f' - 1| {fe[1]:.1e}")
RES["S1"] = dict(f1=str(f1), fp1=str(fp1), fpp1=str(fpp1), fppp1=str(d1_1), fpppp1=str(d2_1), A6=str(A6),
                 knots_C4=knot_c, q_ge_1_exact=ok_hi, F_identities=ok_F, fpp_max=fpp_max, q_at_fpp_max=q_at_max,
                 fpp_min_on_half_to_1=fpp_min_layer, q_fpp_eq_1=q_unit, fprime_monotone=mono)
check("S1", f1 == sp.Rational(1, 2) and fp1 == 1 and fpp1 == 1 and d1_1 == 0 and d2_1 == 0 and ok_hi and ok_F
      and all(knot_c) and mono and A6 == sp.Rational(122363904, 44610575),
      "f = q^2/2 (with f', f'' and the stress term) exactly for q >= 1; C4 joins; f' monotone")

# ================================================================ U4: independent SI estimate of the Galactic phantom
P("\n== U4: independent SI estimate of the Galactic phantom (spherical Hernquist + simple-nu QUMOND; this lane's code)")
X3 = json.load(open(os.path.join(X3D, "x3_switched_stiffness_results.json")))["D2"]
R0 = 8.178; RHO_B0 = 0.08


def nu(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def phantom_sph(r_kpc, Mb, a_kpc, a0):
    """rho_ph = (1 / (4 pi G r^2)) d/dr [r^2 (g - g_N)], SI, returned in Msun/pc^3."""
    def r2dg(r):
        gN = G_SI * Mb * MSUN_SI / (r + a_kpc * KPC_SI) ** 2
        return r * r * (nu(gN / a0) - 1.0) * gN
    r = r_kpc * KPC_SI; h = 1e-4 * r
    return (r2dg(r + h) - r2dg(r - h)) / (2 * h) / (4 * math.pi * G_SI * r * r) / MSUN_PC3_SI


def rho_hern(r_kpc, Mb, a_kpc):
    return Mb * a_kpc / (2 * math.pi * r_kpc * (r_kpc + a_kpc) ** 3) / 1e9          # Msun/pc^3


RRb, ZZb = np.meshgrid(np.linspace(7.2, 9.2, 41), np.linspace(-1.0, 1.0, 41))
rbox = np.sqrt(RRb ** 2 + ZZb ** 2).ravel()
u4 = {}; FACT = {}
for f in FOOTS:
    x3box, x3sun = X3["galactic"][f]["min_box"], X3["galactic"][f]["at_sun"]
    rows = []
    for Mb in (4e10, 6e10, 8e10):
        for aH in (2.0, 3.0, 4.0):
            boxmin = float(min(phantom_sph(r, Mb, aH, A0[f]) for r in rbox))
            gN0 = G_SI * Mb * MSUN_SI / ((R0 + aH) * KPC_SI) ** 2
            sun = phantom_sph(R0, Mb, aH, A0[f]) + (nu(gN0 / A0[f]) - 1) * (RHO_B0 - rho_hern(R0, Mb, aH))
            fb = max(boxmin / x3box, x3box / boxmin); fs = max(sun / x3sun, x3sun / sun)
            rows.append(dict(Mb=Mb, aH_kpc=aH, box_min=boxmin, at_sun=float(sun), factor_box=fb, factor_sun=float(fs)))
    cen = [r_ for r_ in rows if r_["Mb"] == 6e10 and r_["aH_kpc"] == 3.0][0]
    FACT[f] = max(max(r_["factor_box"], r_["factor_sun"]) for r_ in rows)
    u4[f] = dict(rows=rows, central=cen, worst_factor=FACT[f], x3_box_min=x3box, x3_at_sun=x3sun)
    P(f"  [{f}] central (Mb 6e10, aH 3 kpc): box min {cen['box_min']:.4f} (X3 {x3box:.4f}), at Sun {cen['at_sun']:.4f} "
      f"(X3 {x3sun:.4f}) Msun/pc^3; over Mb 4-8e10, aH 2-4 kpc: box min {min(r_['box_min'] for r_ in rows):.4f}-"
      f"{max(r_['box_min'] for r_ in rows):.4f}, at Sun {min(r_['at_sun'] for r_ in rows):.4f}-{max(r_['at_sun'] for r_ in rows):.4f}; "
      f"worst disagreement factor with X3 {FACT[f]:.2f}")
RES["U4"] = u4
check("U4", all(FACT[f] <= 10 for f in FOOTS), f"independent estimate within a factor 10 of X3 on both footings "
      f"(worst {max(FACT.values()):.2f}); the margin below is divided by this factor")

# ================================================================ S2-S4: Sigma/b over the frozen region
P("\n== S2: Sigma/b over the frozen region (R1: X3 D2 rows minus 2.5 x the 1 Msun lobe; R2: near zone)")
s30_pc = 30e3 * AU_SI / PC_SI
S2 = {}
for f in FOOTS:
    rows = [r_ for r_ in X3["rows"] if r_["foot"] == f]
    r1 = [dict(x_e=r_["x_e"], Lstar_pc=r_["Lstar_pc"], Sigma=r_["rho_gal_min"] - 2.5 * r_["max_neg_lobe_Msun_pc3"],
               q=(r_["rho_gal_min"] - 2.5 * r_["max_neg_lobe_Msun_pc3"]) / RHO_DE[f]) for r_ in rows]
    sig2 = min(X3["H4_C3_min"], X3["galactic"][f]["at_sun"])
    q2 = sig2 / RHO_DE[f]
    qmin = min(min(r_["q"] for r_ in r1), q2)
    S2[f] = dict(R1=r1, R2_Sigma=sig2, R2_q=q2, q_min=qmin, q_eff=qmin / FACT[f], rho_DE=RHO_DE[f])
    for r_ in r1:
        P(f"  [{f}] R1 x_e {r_['x_e']}, L* {r_['Lstar_pc']} pc: Sigma {r_['Sigma']:.6f} Msun/pc^3 -> Sigma/b {r_['q']:.4e}")
    P(f"  [{f}] R2 near zone: Sigma {sig2:.4f} Msun/pc^3 -> Sigma/b {q2:.4e}")
    P(f"  [{f}] MIN Sigma/b over R1, R2 = {qmin:.4e}; after U4's factor {FACT[f]:.2f}: {qmin / FACT[f]:.4e}")
RES["S2"] = S2

P("\n== S3: near-zone sign (the binary's own response only raises Sigma where the binary lives)")
s3 = {}
for f in FOOTS:
    rows = [r_ for r_ in X3["rows"] if r_["foot"] == f]
    neg_in = min(r_["neg_r_range_pc"][0] for r_ in rows)
    rho_hh = 0.1 / (2 * math.pi * LFL[f] ** 2 * s30_pc)
    s3[f] = dict(neg_lobes_start_pc=neg_in, ratio_to_30kAU=neg_in / s30_pc, hedgehog_div_0p1Msun_30kAU=rho_hh)
    P(f"  [{f}] negative D.P of a point mass starts at {neg_in:.2f} pc = {neg_in / s30_pc:.0f} x 30 kAU ({s30_pc:.4f} pc); "
      f"hedgehog divergence M/(2 pi L*^2 r) at 30 kAU for 0.1 Msun = +{rho_hh:.3e} Msun/pc^3 (> 0)")
RES["S3"] = s3
check("S3", all(v["ratio_to_30kAU"] >= 100 and v["hedgehog_div_0p1Msun_30kAU"] > 0 for v in s3.values()),
      "negative lobes start >= 100 x the widest DR4 separation; the hedgehog divergence is positive")

P("\n== S4: Galactic inputs")
far = X3["far_effect_estimate"]; s4b = far * max(1.0, fpp_max)
P(f"  x_e = g_obs / a0 is observed (1.778, 1.9, 2.32 e-10 m/s^2): independent of the action.")
P(f"  rho_gal's stiffness dependence (X3 far-region estimate) {far:.2e} x max(1, max f'' = {fpp_max:.3f}) = {s4b:.2e}")
RES["S4"] = dict(far_effect_estimate=far, fpp_max=fpp_max, bound=s4b)
check("S4", s4b < 1e-3, f"blend's effect on rho_gal <= {s4b:.1e} relative (line 1e-3)")

# ================================================================ CHANGED branch machinery: screened local inversion
LU = np.linspace(math.log(1e-12), 0.0, 400001)
UU = np.exp(LU)


def finv(y):
    """(f')^-1, vectorised: 0 for y <= 0, y for y >= 1, bisection on (0, 1) (f' strictly increasing there)."""
    y = np.asarray(y, float); out = np.where(y >= 1.0, y, 0.0)
    m = (y > 0) & (y < 1.0)
    if m.any():
        lo = np.zeros(m.sum()); hi = np.ones(m.sum()); ym = y[m]
        for _ in range(64):
            mid = 0.5 * (lo + hi); up = fblend(mid, 1) < ym
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        out[m] = 0.5 * (lo + hi)
    return out


def blend_factor(q_bg, h_s):
    """Relative acceleration at s under the blend over the raw one; h_s = rho_hh(s)/b, h(u) = h_s/u, u = r/s."""
    fpb = float(fblend(np.array([q_bg]), 1)[0])
    qv = finv(fpb + h_s / UU)
    num = simpson((qv - q_bg) * UU ** 3, x=LU)
    u0 = UU[0]
    num += (fpb - q_bg) * u0 ** 3 / 3 + h_s * u0 ** 2 / 2        # 0 < u < 1e-12: saturated, f' = q
    return num / (h_s / 2)


P("\n== KC: control of the CHANGED-branch method (not a label gate unless the branch is used)")
kc_raw = max(abs(blend_factor(qb, hs) - 1) for qb in (1.0, 2.0, 10.0) for hs in (1e-3, 0.1, 10.0))
yy = np.geomspace(1e-9, float(fblend(np.array([0.5]), 1)[0]), 50)
A_ = float(sp.Rational(form["A"]))
kc_inv = float(np.max(np.abs(finv(yy) / (5 * yy / A_) ** 0.2 - 1)))
P(f"  q_bg >= 1 (raw everywhere): |factor - 1| max {kc_raw:.1e}; (f')^-1 vs analytic (5y/A)^(1/5) on the pure-power piece: max rel {kc_inv:.1e}")
RES["KC"] = dict(raw_factor_dev=kc_raw, inverse_dev=kc_inv)
check("KC", kc_raw <= 1e-9 and kc_inv <= 1e-9, "the local inversion returns the raw answer when Sigma >= b, and inverts f' exactly")

# ================================================================ labels per footing
P("\n== Labels" + (f"  [{MUT}]" if MUT else ""))
MASSES_INV = (0.1, 0.25, 0.5, 1.0, 1.5, 2.5)
base_ok = CHK["K0"] and CHK["KA1"] and CHK["KA2"] and CHK["U2"] and CHK["U3"] and CHK["S1"] and CHK["S4"]
LAB, DET = {}, {}
for f in FOOTS:
    q_eff = S2[f]["q_eff"]
    bmult = 1.0
    if MUT in ("M1", "M1b"):
        target = 0.25 if MUT == "M1" else 0.75
        bmult = S2[f]["q_eff"] / target                      # b raised so the region's minimum sits at q = target
        q_eff = q_eff / bmult
        P(f"  [{f}] {MUT}: b multiplied by {bmult:.4e} -> region minimum Sigma/b = {q_eff:.4f}")
    sealed = np.array(CQ2J["gamma_r"][f"{f}|1.9e-10|M1.0"]["gamma_r_minus_1"])
    miss = [k_ for k_ in ("K0", "KA1", "KA2", "U2", "U3", "S1", "S4") if not CHK[k_]]
    if not base_ok or S2[f]["q_min"] <= 0:
        LAB[f] = "NOT EVALUABLE"
        DET[f] = dict(missing=miss, q_min=S2[f]["q_min"])
        P(f"  [{f}] NOT EVALUABLE: failed {miss}" + ("; Sigma <= 0 in the region" if S2[f]["q_min"] <= 0 else ""))
        continue
    if q_eff >= 1.0 and CHK["S3"]:
        LAB[f] = "MARGIN HOLDS, UNCHANGED"
        DET[f] = dict(q_min=S2[f]["q_min"], q_eff=q_eff, gamma_r_minus_1_30kAU=float(sealed[-1]))
        P(f"  [{f}] MARGIN HOLDS, UNCHANGED: min Sigma/b {S2[f]['q_min']:.4e} (after U4 {q_eff:.4e}) >= 1; the blend equals "
          f"the raw form with F', F'' and the stress term on the whole region; sealed gamma_r - 1 at 30 kAU {sealed[-1]:.4e} stands")
        continue
    # CHANGED branch: screened local inversion, worst over masses, every s
    b_msun = bmult * RHO_DE[f]
    L_pc = LFL[f]
    grid = {}
    for M in MASSES_INV:
        fac = []
        for s in S_KAU:
            s_pc = s * 1e3 * AU_SI / PC_SI
            hs = M / (2 * math.pi * L_pc ** 2 * s_pc) / b_msun
            fac.append(float(blend_factor(q_eff, hs)))
        grid[f"M{M}"] = fac
    worst = np.max(np.array([grid[f"M{M}"] for M in MASSES_INV]), axis=0)     # worst (largest) over source masses
    recomputed = sealed * worst
    exceed = recomputed > sealed * (1 + 1e-9)
    newt = float(recomputed.max()) <= 1e-3
    LAB[f] = "MARGIN FAILS" if exceed.any() else "MARGIN HOLDS, CHANGED"
    DET[f] = dict(q_eff=q_eff, b_mult=bmult, factor_grid=grid, worst_factor=worst.tolist(), recomputed=recomputed.tolist(),
                  sealed=sealed.tolist(), newtonian_line_holds=newt, max_over_dr4_sigma=float(recomputed.max() / 0.02))
    P(f"  [{f}] region minimum q_bg {q_eff:.4f}: worst factor over M 0.1-2.5 Msun by s: " + " ".join(f"{v:.3f}" for v in worst))
    P(f"  [{f}] recomputed gamma_r - 1: " + " ".join(f"{v:.3e}" for v in recomputed) + f"  (sealed 30 kAU {sealed[-1]:.3e})")
    P(f"  [{f}] {LAB[f]}; CQ2's NEWTONIAN line (<= 1e-3) {'holds' if newt else 'FAILS'}; max / DR4 sigma 0.02 = "
      f"{recomputed.max() / 0.02:.1e}")
RES["labels"] = LAB; RES["label_detail"] = DET

# ================================================================ hand estimate (main run only)
if not MUT:
    P("\n== The lead's hand estimate (D.P 0.0055-0.045 Msun/pc^3, rho_DE ~ 1e-7 Msun/pc^3, Sigma/b ~ 1e4-1e5, blend = raw)")
    rde_ok = all(1e-7 / 3 <= RHO_DE[f] <= 3e-7 for f in FOOTS)
    qmins = {f: S2[f]["q_min"] for f in FOOTS}
    qsun = {f: S2[f]["R2_q"] for f in FOOTS}
    ratio_ok = all(10 ** 3.5 <= v <= 10 ** 5.5 for v in qmins.values())
    lab_ok = all(LAB[f] == "MARGIN HOLDS, UNCHANGED" for f in FOOTS)
    grade = "RIGHT" if (rde_ok and ratio_ok and lab_ok and CHK["U2"] and CHK["U3"]) else "WRONG"
    P(f"  rho_DE {RHO_DE['canonical']:.3e} / {RHO_DE['alt']:.3e} Msun/pc^3 (order 1e-7: {rde_ok}); min Sigma/b "
      f"{qmins['canonical']:.3e} / {qmins['alt']:.3e} (order 1e4-1e5: {ratio_ok}); at the Sun {qsun['canonical']:.3e} / "
      f"{qsun['alt']:.3e}; same quantity and units (U2, U3): {CHK['U2'] and CHK['U3']}; blend = raw on the region: {lab_ok}")
    P(f"  GRADE: {grade}")
    RES["hand_estimate"] = dict(grade=grade, rho_DE=RHO_DE, q_min=qmins, q_sun=qsun, rule="rho_DE within x3 of 1e-7; "
                                "min Sigma/b within 10^3.5-10^5.5; both labels UNCHANGED; U2 and U3 pass")

# ================================================================ exit
if MUT:
    if MUT in ("M1", "M1b"):
        bites = all(LAB[f] != "MARGIN HOLDS, UNCHANGED" for f in FOOTS)
        why = f"labels {LAB} (must not be UNCHANGED)"
    elif MUT == "M2":
        bites = not CHK["KA2"]; why = f"KA2 {'FAIL' if not CHK['KA2'] else 'PASS'} (must FAIL)"
    else:
        bites = not CHK["U2"]; why = f"U2 {'FAIL' if not CHK['U2'] else 'PASS'} (must FAIL)"
    RES["mutate_bites"] = bites
    P(f"\nMUTATE {MUT}: {'BITES' if bites else 'DOES NOT BITE (machinery blind)'}: {why}")
    code = 1 if bites else 0
else:
    for f in FOOTS:
        P(f"\nLABEL [{f}]: {LAB[f]}")
    code = 0 if all(LAB[f] != "NOT EVALUABLE" for f in FOOTS) and base_ok and CHK["S3"] and CHK["KC"] else 1
RES["wall_s"] = time.time() - T0
P(f"\nwall {RES['wall_s']:.1f} s; exit {code}")
P(HDR)
open(os.path.join(HERE, f"cqb1{SFX}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"cqb1{SFX}.json"), "w"), indent=1, default=float)
sys.exit(code)
