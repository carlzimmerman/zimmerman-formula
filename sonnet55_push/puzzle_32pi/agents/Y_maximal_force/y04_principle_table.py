"""Lane Y, script 4: the principle table of PREDECLARED.md (Part C combinations, including the force balance C6),
the Lambda = 0 control, the mutation controls, and the census of fixed outputs against targets and decoys."""
import json
import os
import mpmath as mp
from common import Ledger, HERE
import cmetric as cm

L_ = Ledger("y04_principle_table")
mp.mp.dps = 50
TARGETS = {"T6": mp.mpf(1) / 6, "T2": mp.mpf(1) / 2, "TF": mp.sqrt(3 / (32 * mp.pi))}
DECOYS = {f"1/{n}": mp.mpf(1) / n for n in (3, 4, 5, 7, 8, 9, 10, 12)}


# ---------------------------------------------------------------- closed forms on the extremal boundary (derived by hand, checked below)
def th_of_q(q):
    return (mp.pi - 2 * mp.atan(q)) / 3            # theta_0, 27 s^2 = q^2/(1+q^2) = sin^2 phi, tan phi = q


def four_mu(t0):                                     # string force / F_max on the extremal boundary
    return 1 - mp.sin(t0) / mp.sin(2 * mp.pi / 3 - t0)


def a_ext(t0):                                       # a = H^2 Area/(4 pi) of the degenerate horizon
    return (2 / mp.sqrt(3)) * mp.sin(t0) * mp.sin(mp.pi / 6 - t0 / 2) / mp.cos(3 * t0 / 2)


def q_of_th(t0):
    return 1 / mp.tan(3 * t0 / 2)


def solve_balance(cfac, afac=1, lo="0.02", hi="1.0"):
    """root of  four_mu(t0) = cfac * afac * a_ext(t0)  on the extremal boundary (theta_0 in (0, pi/3))"""
    f = lambda t0: four_mu(t0) - cfac * afac * a_ext(t0)
    t0 = mp.findroot(f, (mp.mpf(lo), mp.mpf(hi)), solver="anderson", tol=mp.mpf("1e-40"), maxsteps=200)
    return t0, q_of_th(t0)


print("\n== checks that the closed forms equal the root-based numerics of cmetric.py ==")
errs = []
for q in ["0.05", "0.3", "1", "2.4", "9"]:
    q = mp.mpf(q)
    s = q / (mp.sqrt(27) * mp.sqrt(1 + q**2))
    h = 1 / q
    t0 = th_of_q(q)
    e1 = abs(4 * cm.mu_string_south(s) - four_mu(t0))
    e2 = abs(cm.horizon_area_over_4piL2(s, h * (1 - mp.mpf("1e-44"))) - a_ext(t0))
    errs.append(max(e1, e2))
L_.check(f"four_mu(theta_0) and a_ext(theta_0) reproduce the numerical string force and horizon area on the extremal boundary (max error {mp.nstr(max(errs), 3)})", max(errs) < mp.mpf("1e-18"))
L_.check("limits: a_ext -> 1/3 as A/H -> 0 (Nariai SdS: horizon radius L/sqrt 3, area 4 pi L^2/3) and -> 0 as A/H -> infinity",
         abs(a_ext(th_of_q(mp.mpf("1e-9"))) - mp.mpf(1) / 3) < mp.mpf("1e-8") and a_ext(th_of_q(mp.mpf("1e9"))) < mp.mpf("1e-8"))

# ---------------------------------------------------------------- C6 area formula check: H -> 0 limit gives 1 - 4 mu (punctured horizon)
print("\n== C6 area formula: as H -> 0 at fixed s, H^2 Area/(4 pi) -> 1 - 4 mu (a straight string through a dS horizon removes the solid-angle fraction 4 mu) ==")
for sv in ["0.03", "0.1", "0.17"]:
    sv = mp.mpf(sv)
    a_small = cm.horizon_area_over_4piL2(sv, mp.mpf("1e-12"))
    L_.check(f"s = {mp.nstr(sv, 3)}: a(h = 1e-12) = {mp.nstr(a_small, 12)}, 1 - 4 mu = {mp.nstr(1 - 4 * cm.mu_string_south(sv), 12)}",
             abs(a_small - (1 - 4 * cm.mu_string_south(sv))) < mp.mpf("1e-9"))
L_.check("and a(m = 0) = 1: horizon area 4 pi L^2 (checked at s -> 0, h = 1)", abs(cm.horizon_area_over_4piL2(mp.mpf("1e-12"), 1) - 1) < mp.mpf("1e-8"))
L_.must_fail("control: a(s = 0.1, h -> 0) is NOT 1 (the string does change the horizon area)", abs(cm.horizon_area_over_4piL2(mp.mpf("0.1"), mp.mpf("1e-12")) - 1) < 0.01)

# ---------------------------------------------------------------- R1 + C6 + C4 : the only two-condition point with Lambda > 0
print("\n== R1 + C6 + C4: force balance 4 mu = 6 a on the extremal boundary ==")
t0, qstar = solve_balance(6)
s_star = qstar / (mp.sqrt(27) * mp.sqrt(1 + qstar**2))
mu_star = cm.mu_string_south(s_star)
print(f"   theta_0* = {mp.nstr(t0, 30)}   q* = A/H = {mp.nstr(qstar, 30)}   s* = mA = {mp.nstr(s_star, 20)}   string force/F_max = {mp.nstr(4*mu_star, 20)}")
L_.check(f"the balance has exactly one solution on the boundary (sign change of 4 mu - 6 a between A/H -> 0 (value -2) and A/H -> infinity (value +1): f(0+) = {mp.nstr(four_mu(th_of_q(mp.mpf('1e-9'))) - 6*a_ext(th_of_q(mp.mpf('1e-9'))), 6)}, f(inf) = {mp.nstr(four_mu(th_of_q(mp.mpf('1e9'))) - 6*a_ext(th_of_q(mp.mpf('1e9'))), 6)}); strictly monotone on 60 grid points",
         four_mu(th_of_q(mp.mpf("1e-9"))) - 6 * a_ext(th_of_q(mp.mpf("1e-9"))) < 0 < four_mu(th_of_q(mp.mpf("1e9"))) - 6 * a_ext(th_of_q(mp.mpf("1e9")))
         and all((four_mu(t) - 6 * a_ext(t)) > (four_mu(t + mp.mpf("0.01")) - 6 * a_ext(t + mp.mpf("0.01"))) for t in [mp.mpf(k) / 60 * (mp.pi / 3 - mp.mpf("0.02")) + mp.mpf("0.005") for k in range(0, 55)]))
resid = abs(four_mu(t0) - 6 * a_ext(t0))
L_.check(f"balance residual {mp.nstr(resid, 3)} at the root (50-digit arithmetic); root also confirmed by the independent root-based numerics: 4 mu(s*) = {mp.nstr(4*mu_star, 12)}", resid < mp.mpf("1e-40") and abs(4 * mu_star - four_mu(t0)) < mp.mpf("1e-15"))
hits = [k for k, v in list(TARGETS.items()) + list(DECOYS.items()) if abs(qstar - v) < mp.mpf("1e-10")]
L_.check(f"outcome FIXED-NON-TARGET: q* = {mp.nstr(qstar, 15)} matches none of the targets or decoys (T6 0.1667, T2 0.5, TF 0.1727: it is 14x, 4.9x, 14x larger)", hits == [])
near_sqrt6 = abs(qstar - mp.sqrt(6))
L_.must_fail(f"control: a percent-level or 1e-3-level coincidence is not a hit; q* is not sqrt 6 = {mp.nstr(mp.sqrt(6), 10)} (differs by {mp.nstr(near_sqrt6, 3)}), not any of the tested constants", near_sqrt6 < mp.mpf("1e-6"))
print("   mpmath.findpoly(q*, degree <= 6, maxcoeff 5000) =", mp.findpoly(qstar, 6, maxcoeff=5000))

# ---------------------------------------------------------------- R1 + C6 alone : a curve, i.e. FAMILY
print("\n== R1 + C6 alone: zero set of 4 mu - 6 a in the interior (s, h) ==")
def D(s, h):
    return 4 * cm.mu_string_south(s) - 6 * cm.horizon_area_over_4piL2(s, h)


s14 = mp.findroot(lambda sv: cm.mu_string_south(sv) - mp.mpf(3) / 14, (mp.mpf("0.05"), cm.SQRT27_INV * (1 - mp.mpf("1e-9"))), solver="anderson", tol=mp.mpf("1e-30"), maxsteps=200)
L_.check("s at mu = 3/14 lies inside the family, 0 < s < 1/sqrt 27", 0 < s14 < cm.SQRT27_INV)
L_.check(f"H -> 0 end of the curve: mu = 3/14 exactly (4 mu = 6(1 - 4 mu) => mu = 3/14), s = mA = {mp.nstr(s14, 12)}; string force = 6/7 F_max", abs(cm.mu_string_south(s14) - mp.mpf(3) / 14) < mp.mpf("1e-30"))
pts = []
for frac in ["0.05", "0.2", "0.4", "0.6", "0.8", "0.95"]:
    sv = s14 + (s_star - s14) * mp.mpf(frac)
    hmax = cm.h_extremal(sv) * (1 - mp.mpf("1e-25"))
    hb = mp.findroot(lambda hv: D(sv, hv), (hmax * mp.mpf("1e-3"), hmax), solver="anderson", tol=mp.mpf("1e-30"), maxsteps=200)
    pts.append((sv, hb, 1 / hb))
    print(f"   s = {mp.nstr(sv, 8)}   h = {mp.nstr(hb, 8)}   q = A/H = {mp.nstr(1/hb, 8)}   (extremal h_max = {mp.nstr(hmax, 8)})")
L_.check("the balance holds on a whole curve q_bal(s): q runs from infinity at (mu = 3/14) down to q* at the extremal boundary; P_bal alone leaves A/H FREE (label FAMILY)",
         all(pts[i][2] > pts[i + 1][2] for i in range(len(pts) - 1)) and pts[0][2] > 5 and abs(pts[-1][2] - qstar) < 0.3)

# ---------------------------------------------------------------- C3 with anything
print("\n== R1 + C3 (+C6): saturation ==")
hpos = mp.mpf("0.05")
Fmaxval = max(-(1 + hpos**2) + yv**2 - 2 * cm.SQRT27_INV * yv**3 for yv in [mp.mpf(k) / 200 for k in range(0, 1200)])
L_.check(f"R1 + C3 + C6: at s = 1/sqrt 27 and h = 0.05 the maximum of F(y) over y in [0, 6) is {mp.nstr(Fmaxval, 6)} < 0 (= -h^2 at y = 1/(3s)): no horizon, no area, no balance: EMPTY. At h = 0 the force is F_max while F_Lambda = 0",
         Fmaxval < 0 and abs(Fmaxval + hpos**2) < mp.mpf("1e-4"))

# ---------------------------------------------------------------- controls
print("\n== Control (a): Lambda = 0 ==")
L_.check("h = 0: the extremal condition 27 s^2 (1 + h^2) = 1 coincides with saturation 27 s^2 = 1 (P_ext <=> P_sat), and A is NOT constrained at all: the principles fix m A, never A alone",
         abs(cm.h_extremal(cm.SQRT27_INV)) < mp.mpf("1e-24"))
qh = lambda q: four_mu(th_of_q(q))
L_.check("A/H -> infinity: the largest static string force -> F_max (the Lambda = 0 saturation) and A/H -> 0: -> 0 (SdS Nariai: no string)", qh(mp.mpf("1e12")) > 1 - mp.mpf("1e-6") and qh(mp.mpf("1e-12")) < mp.mpf("1e-6"))

print("\n== Control (c): mutations of the ingredients move the balance point ==")
muts = {
    "base (deficit 8 pi G mu, rho = Lambda/8 pi, area 4 pi)": (6, 1),
    "deficit 4 pi G mu (tension 2 mu for the same geometry): balance 4 mu = 3 a": (3, 1),
    "rho = Lambda/(4 pi): balance 4 mu = 12 a": (12, 1),
    "horizon area 2 pi (instead of 4 pi): balance 4 mu = 3 a": (3, 1),
    "period of z doubled (kappa -> 2 kappa, area x2): balance 4 mu = 12 a": (6, 2),
}
qm = {}
for name, (cf, af) in muts.items():
    tt, qq = solve_balance(cf, af)
    qm[name] = qq
    print(f"   {name:75s} q* = {mp.nstr(qq, 12)}")
base = qm["base (deficit 8 pi G mu, rho = Lambda/8 pi, area 4 pi)"]
L_.must_fail("mutation 'rho = Lambda/(4 pi)' leaves q* unchanged", abs(qm["rho = Lambda/(4 pi): balance 4 mu = 12 a"] - base) < mp.mpf("1e-6"))
L_.must_fail("mutation 'deficit 4 pi G mu' leaves q* unchanged", abs(qm["deficit 4 pi G mu (tension 2 mu for the same geometry): balance 4 mu = 3 a"] - base) < mp.mpf("1e-6"))
L_.check("mutations 'rho = Lambda/4 pi' and 'period doubled' coincide (both multiply a by 2), 'deficit 4 pi' and 'area 2 pi' coincide (both halve the ratio): the algebra behaves as it should",
         abs(qm["rho = Lambda/(4 pi): balance 4 mu = 12 a"] - qm["period of z doubled (kappa -> 2 kappa, area x2): balance 4 mu = 12 a"]) < mp.mpf("1e-25")
         and abs(qm["deficit 4 pi G mu (tension 2 mu for the same geometry): balance 4 mu = 3 a"] - qm["horizon area 2 pi (instead of 4 pi): balance 4 mu = 3 a"]) < mp.mpf("1e-25"))
print("   (note: the purely geometric outcomes C3 saturation s = 1/sqrt 27 and the C4 extremal curve do not contain the tension-normalisation constants, so those mutations are not controls for them)")

# ---------------------------------------------------------------- summary table + census
rows = [
    ("R1", "FAMILY", "q free", "two parameters (m A, A/H); nothing fixes them"),
    ("R1 + C2 (P_none)", "EMPTY (m A != 0) / q FREE at m A = 0", "-", "no string and no strut is possible only without mass or acceleration"),
    ("R1 + C3 (P_sat)", "ENDPOINT", "q = infinity", "saturation 27 m^2 A^2 = 1 leaves no static region at Lambda > 0"),
    ("R1 + C4 (P_ext)", "FAMILY (curve)", "q in (0, infinity)", "largest force F_max [1 - sin th/sin(2 pi/3 - th)], th = (pi - 2 arctan(A/H))/3"),
    ("R1 + C3 + C4", "ENDPOINT", "q = infinity", "only as H -> 0"),
    ("R1 + C5 (P_eq)", "= C4 (boundary only)", "-", "T_bh > T_(acc/cosm) strictly in the interior"),
    ("R1 + C6 (P_bal)", "FAMILY (curve)", f"q in ({mp.nstr(qstar, 6)}, infinity)", "curve ends at mu = 3/14 (H -> 0) and at the extremal point"),
    ("R1 + C6 + C4", "FIXED-NON-TARGET", f"q* = {mp.nstr(qstar, 15)}", f"string force {mp.nstr(4*mu_star, 10)} F_max, mA = {mp.nstr(s_star, 10)}"),
    ("R1 + C6 + C3", "EMPTY", "-", "no horizon at saturation for h > 0"),
]
print("\n== Principle table ==")
for r in rows:
    print("   ", " | ".join(r))
fixed_q = {"S3 M_a": mp.mpf(1) / 2, "S3 M_b": mp.mpf(1) / 4, "S3 M_c": 3 * mp.sqrt(3) / 4, "S3 M_d": mp.mpf(1) / 4, "S3 M_e": mp.mpf(1) / 6,
           "S3 M_f": 2 / (3 * mp.pi), "S3 M_g": 1 / (3 * mp.pi), "C  R1+C6+C4": qstar}
print("\n== Census of every FIXED output (S3 masses and the one fixed C-metric point) against targets and decoys ==")
th = {}
dh = {}
for k, v in fixed_q.items():
    t_ = [n for n, tv in TARGETS.items() if abs(v - tv) < mp.mpf("1e-30")]
    d_ = [n for n, dv in DECOYS.items() if abs(v - dv) < mp.mpf("1e-30")]
    th[k] = t_; dh[k] = d_
    print(f"   {k:14s} q = {mp.nstr(v, 12):>16s}   target hits {t_}   decoy hits {d_}")
n_t = sum(len(v) for v in th.values()); n_d = sum(len(v) for v in dh.values())
L_.check(f"census: 8 fixed outputs, {n_t} target hits (M_a -> T2 = the Hubble-sphere field; M_e -> T6, void because M_e was built after the target), {n_d} decoy hits (1/4 twice); zero target hits among the C-metric outputs; TF never",
         n_t == 2 and n_d == 2 and th["C  R1+C6+C4"] == [] and not any("TF" in v for v in th.values()))
L_.check("no hit comes from an exact construction with all parameters fixed by a declared principle and a non-restated mass: DERIVATION criterion NOT met",
         th["S3 M_e"] == ["T6"] and th["C  R1+C6+C4"] == [])

out = {"q_star": str(qstar), "s_star": str(s_star), "string_force_over_Fmax_star": str(4 * mu_star), "theta0_star": str(t0),
       "mu_3_14_s": str(s14), "mutations_q_star": {k: str(v) for k, v in qm.items()},
       "table": rows, "census": {k: {"q": str(v), "targets": th[k], "decoys": dh[k]} for k, v in fixed_q.items()}}
json.dump(out, open(os.path.join(HERE, "y04_results.json"), "w"), indent=1)
L_.finish()
