"""CFG910 post-hoc verification (NOT pre-registered; written after the real run, disclosed in the README).

Purpose: the graded verdict of cfg910_d01.py (G1 has no admissible root) rests on the vertex classes computed in the Landau-type
gauges by restricting the graviton to the kernel of the gauge condition.  The pre-registered gates test that restriction only on the
two-point function (G-BF).  This script tests it on the vertex classes: the full 10-component graviton with a FINITE gauge-fixing
weight beta (CPR condition chi_nu = d^mu h_mu nu - (1/4) d_nu h, and the beta = 1 de Donder condition for LdD), regulated type I like
every other kinetic term, at beta = 1e4, 1e5, 1e6 (exact rational arithmetic), Richardson-extrapolated to beta -> infinity, must
reproduce the kernel-restricted class coefficients at the background point (eta_h = -2, lambda_3 = lambda_2 = lambda*, xi = 1).
It then recomputes G1's (a, b) from the extrapolated classes, and tabulates the decomposition of Delta that decides the root.

Machinery: sections (0)-(2) of cfg910_d01.py are executed verbatim (exec of its source text up to section (3)), so the vertex builder,
expansion and fit are the committed ones; nothing in cfg910_d01.py is changed.
Usage: OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg910_landau_check.py    -> exit 0 iff the extrapolation reproduces the restriction.
First execution (cfg910_landau_check_FIRSTRUN.out/.json, kept): LdD flagged because the deviation was divided by each component;
the [U1 V1] class has c_A = 0 exactly (extrapolated 2.3e-12).  Only that metric line changed (deviation / class scale)."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = (HERE / "cfg910_d01.py").read_text()
CUT = SRC.index("# ================================================================== (3) G-VTX")
sys.argv = [str(HERE / "cfg910_d01.py"), "NORMAL"]
NS = {"__file__": str(HERE / "cfg910_d01.py"), "__name__": "cfg910_d01_sections_0_2"}
exec(compile(SRC[:CUT], str(HERE / "cfg910_d01.py"), "exec"), NS)

sp, np, json = NS["sp"], NS["np"], NS["json"]
Q, I_, ZN, E4, I4 = NS["Q"], NS["I_"], NS["ZN"], NS["E4"], NS["I4"]
Hm_, Hp_, kap, eta, L3, xi = NS["Hm_"], NS["Hp_"], NS["kap"], NS["eta"], NS["L3"], NS["xi"]
eh_bil, mass_bil, gf_fdd_bil, photon_bil, bil2mat = NS["eh_bil"], NS["mass_bil"], NS["gf_fdd_bil"], NS["photon_bil"], NS["bil2mat"]
per_config_mats, class_traces, radial, fit_2pt, fit_vertex = NS["per_config_mats"], NS["class_traces"], NS["radial"], NS["fit_2pt"], NS["fit_vertex"]
run_classes, CONFIGS, CONFIG_REFL, VCLASSES, stamp, agf = NS["run_classes"], NS["CONFIGS"], NS["CONFIG_REFL"], NS["VCLASSES"], NS["stamp"], NS["agf"]
LSTAR, GSTAR = NS["LSTAR"], NS["GSTAR"]
print = NS["print"]
fails = []


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)


LAM = sp.Rational(LSTAR).limit_denominator(10**12)
PT = {eta: -2, L3: LAM}
XI1 = Q(1)


def gf_cpr_bil(Xm, Xp, s):
    """(Z_N bg/2) s |chi|^2, chi_nu = q-hat^mu X_mu nu - (1/4) q-hat_nu tr X (rho = 0), positive weight, delta background."""
    def chi(X, sg):
        trX = X.trace()
        return [sg * I_ * (sum(E4[n] * X[n, mu] for n in range(4)) - Q(1, 4) * E4[mu] * trX) for mu in range(4)]
    cm, cp = chi(Xm, -1), chi(Xp, +1)
    bg = sp.Symbol("bg", positive=True)
    return ZN * bg / 2 * s * sum(cm[m] * cp[m] for m in range(4)), bg


def brute_classes(kind, beta):
    """Full 14-component computation with a finite gauge-fixing weight beta (kind 'CPR' or 'LdD'), at PT, xi = 1."""
    Bh = ZN * (Q(1, 2) * (eh_bil(Hm_, Hp_, I4, 1, E4, 1) + eh_bil(Hp_, Hm_, I4, 1, E4, 1)))
    if kind == "CPR":
        Bg, bg = gf_cpr_bil(Hm_, Hp_, 1)
        Bh += Bg.subs(bg, beta)
    else:
        Bh += ZN * gf_fdd_bil(Hm_, Hp_, I4, 1, E4, 1).subs(agf, beta)
    Bm = ZN * 2 * LAM * mass_bil(Hm_, Hp_, I4, 1)
    Bk, Bgf = photon_bil(I4, 1, E4, 1, XI1)
    Mkh = bil2mat(Bh)
    Mka = bil2mat(Bk + Bgf)
    M0 = Mkh + bil2mat(Bm) + Mka
    dR0 = (2 * (Mkh + Mka) + 2 * (1 - kap**2) * Mkh)          # eta_h = -2: -eta (1 - kappa^2) Mkh = +2 (1 - kappa^2) Mkh
    G = M0.inv()
    S = (G * dR0 * G).applyfunc(sp.expand)
    vals = {k: [] for k in ["2pt_V1V1", "2pt_V2"] + VCLASSES}
    for Hc, Fb in CONFIGS + [CONFIG_REFL]:
        m = per_config_mats(Hc, Fb, "fl", LAM, LAM, -2, XI1)
        tr_ = class_traces(m, G, S, "FdD")                    # 'FdD' = no restriction (full 14 components)
        for k, v in tr_.items():
            vals[k].append(radial(v))
    out = {}
    for k in ("2pt_V1V1", "2pt_V2"):
        out[k] = float(sp.N(fit_2pt(vals[k])[0]))
    for k in VCLASSES:
        cA, cB, _, _ = fit_vertex(vals[k])
        out[k] = (float(sp.N(cA)), float(sp.N(cB)))
    return out


def a_b(cls):
    c0 = cls["2pt_V1V1"] + cls["2pt_V2"]
    cb = {k: (cls[k][1] if isinstance(cls[k], tuple) else cls[k]) for k in VCLASSES}
    a = -4 * c0 - 2 * (cb["g5"] + cb["g4"] + cb["g3"])
    b = -2 * (cb["g4h"] + cb["g3h"])
    return a, b, c0


report = {}
for kind in ("CPR", "LdD"):
    print(f"\n== {kind}: kernel restriction (as graded) vs finite gauge-fixing weight beta -> infinity (eta_h = -2, lambda_3 = lambda*, xi = 1)")
    ref_raw, _, _, _ = run_classes("fl", kind, LAM, LAM, -2, XI1, f"restricted {kind}")
    ref = {k: (tuple(float(sp.N(x)) for x in v) if isinstance(v, tuple) else float(sp.N(v))) for k, v in ref_raw.items()}
    br = {}
    for beta in (Q(10**4), Q(10**5), Q(10**6)):
        br[int(beta)] = brute_classes(kind, beta)
        stamp(f"brute {kind} beta = {int(beta)}")
    ext = {}
    worst = 0.0
    for k in ref:
        if isinstance(ref[k], tuple):
            e_ = tuple((10 * br[10**6][k][i] - br[10**5][k][i]) / 9 for i in range(2))
            dev = max(abs(e_[i] - ref[k][i]) for i in range(2)) / max(abs(ref[k][0]), abs(ref[k][1]))   # relative to the class scale (amended after the first run: a c_A that is exactly 0 made the per-component ratio meaningless)
            first = abs(br[10**4][k][1] - ref[k][1])
            print(f"   {k:9s} c_B: restricted {ref[k][1]:+.10f}; beta 1e4 {br[10**4][k][1]:+.10f}, 1e5 {br[10**5][k][1]:+.10f}, "
                  f"1e6 {br[10**6][k][1]:+.10f}; extrapolated {e_[1]:+.10f} (rel dev {dev:.1e}; |dev at 1e4| {first:.1e})")
        else:
            e_ = (10 * br[10**6][k] - br[10**5][k]) / 9
            dev = abs(e_ - ref[k]) / max(abs(ref[k]), 1e-12)
            print(f"   {k:9s} c_0: restricted {ref[k]:+.10f}; beta 1e6 {br[10**6][k]:+.10f}; extrapolated {e_:+.10f} (rel dev {dev:.1e})")
        ext[k] = e_
        worst = max(worst, dev)
    chk(f"LANDAU {kind}", worst < 1e-6, f"Richardson-extrapolated finite-beta classes reproduce the kernel restriction (worst relative deviation {worst:.1e})")
    a_r, b_r, c0_r = a_b(ref)
    a_e, b_e, _ = a_b(ext)
    print(f"   G1-type closure (eta_h = -2, lambda_3 = lambda*, g_4 = g_5 = g_3): restricted a = {a_r:+.8f}, b = {b_r:+.8f}; "
          f"extrapolated a = {a_e:+.8f}, b = {b_e:+.8f}; root needs -b/a > 0: {(-b_r / a_r) > 0}")
    report[kind] = dict(restricted=ref, extrapolated=ext, worst_rel_dev=worst, a=a_r, b=b_r, c0=c0_r)

# ---- decomposition of Delta at the graded point (CPR), from the restricted classes
print("\n== Decomposition of Delta = a g_3 + b sqrt(g_3 g*) at G1's point (CPR), per unit coupling")
r = report["CPR"]["restricted"]
c0 = r["2pt_V1V1"] + r["2pt_V2"]
cb = {k: r[k][1] for k in VCLASSES}
terms = {"eta_A^grav (-4 c_0)": -4 * c0, "[U2] (aahhh tadpole)": -2 * cb["g5"], "[U1 V1] (aahh x aah)": -2 * cb["g4"],
         "[V1 V1 W_A] (photon-line h_c)": -2 * cb["g3"], "[V2 W_h] (graviton-line h_c, tadpole)": -2 * cb["g4h"],
         "[V1 V1 W_h] (graviton-line h_c, loop)": -2 * cb["g3h"]}
for k, v in terms.items():
    print(f"   {k:40s} {v:+.8f}")
a_, b_ = report["CPR"]["a"], report["CPR"]["b"]
print(f"   a = {a_:+.8f} (sum of the first four), b = {b_:+.8f} (sum of the last two)")
print(f"   at the background line g_3 = g*: Delta/g* = a + b = {a_ + b_:+.8f}, i.e. {(a_ + b_) / (-4 * c0) * 100:+.1f}% of eta_A^grav per unit coupling "
      f"(the covariant regulator gives exactly 0)")
print(f"   charged-matter bracket of the pre-registration: +/- eta_A^matter = +/- 2 f_g = +/- {4 * c0:.8f} per unit g_3, i.e. {4 * c0 / abs(a_):.1f} x |a|")
report["decomposition"] = dict(terms=terms, a=a_, b=b_, bf_line_residual=a_ + b_, matter_bracket=4 * c0)
with open(HERE / "cfg910_landau_check.json", "w") as fh:
    json.dump(report, fh, indent=1, default=float)
print(f"\nCHECKS FAILED: {fails if fails else 'none'}")
stamp("done")
sys.exit(1 if fails else 0)
