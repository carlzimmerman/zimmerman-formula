# -*- coding: utf-8 -*-
"""CFG172 A3 -- G6 (preferred-frame alphas) and G7 (a0 vs speed through the flow frame).  Frozen: sec. 2 (G6, G7), 4 (C3, C4, M5).
G7: RE-DERIVED here (not imported from KM1/L333): the quadratic action of khronometric gravity in unitary gauge, N = 1 + phi, N_i = d_i B,
    gamma_ij = (1 - 2 psi) delta_ij, S = (1/16 pi G) int N sqrt(gamma)[K_ij K^ij - (1 + c2) K^2 + R3 + c14 a_i a^i] + S_m, with a
    momentumless lapse source rho_ph (the KM1 modelling of the MOND phantom) moving at v; steady solution f(x - v t) in Fourier space;
    the aether-acceleration potential phi expanded to O(v^2):  phi = phi_static (1 + C v^2 mu^2), mu = cos(angle between k and v).
    Deep-MOND profile -> radial input distortion C v^2/3 (isotropic) and tilt amplitude C v^2/3 (sympy).
G6: alpha_1 = -4 c14, alpha_2 = c14 (c14 - c2 + 2 c14 c2)/(c2 (2 - c14)) are the QUOTED formulas (KM3 / L333 header; Yagi et al. 2014 as the record quotes them);
    NOT re-derived here (declared departure).  Limits 3.4e-5 (frozen) and 3.5e-5 (data-chat note), alpha_2 <= 1.6e-9: from memory, unverified.
MUTATE = M5 (w = 3000 km/s instead of 600: the G7 cell of 11C-a/-c at c2 = 5e-4 must flip to FAIL)."""
import sympy as sp
from sympy.calculus.euler import euler_equations
from cfg172_common import *

R = Run("CFG172_A3_ppn_frame")
mut = R.mut
W_KMS = 3000.0 if mut == "M5" else 600.0

# ---- sympy: quadratic action, static check, moving source --------------------------------------------------------------------
t, x, y, z = sp.symbols("t x y z"); c2, c14, Gs, v, k, mu = sp.symbols("c2 c14 G v k mu", positive=True)
ph = sp.Function("phi")(t, x, y, z); ps = sp.Function("psi")(t, x, y, z); B = sp.Function("B")(t, x, y, z)
rb = sp.Function("rb")(t, x, y, z); rp = sp.Function("rp")(t, x, y, z)
lap = lambda f: sp.diff(f, x, 2) + sp.diff(f, y, 2) + sp.diff(f, z, 2)
grad2 = lambda f: sp.diff(f, x) ** 2 + sp.diff(f, y) ** 2 + sp.diff(f, z) ** 2
psd = sp.diff(ps, t)
# K_ij = -psi_dot delta_ij - d_i d_j B ;  K_ijK^ij - (1+c2)K^2 = -6 psi_dot^2 - 4 psi_dot lap B - c2 (3 psi_dot + lap B)^2  (by parts);
# N sqrt(gamma) R3 at 2nd order = 2 (grad psi)^2 + 4 phi lap psi ; c14 (grad phi)^2 ; matter: -rho phi + rho_b v d_z B
Lgrav = -6 * psd ** 2 - 4 * psd * lap(B) - c2 * (3 * psd + lap(B)) ** 2 + 2 * grad2(ps) + 4 * ph * lap(ps) + c14 * grad2(ph)
L = Lgrav - 16 * sp.pi * Gs * ((rb + rp) * ph - rb * v * sp.diff(B, z))
eqs = euler_equations(L, [ph, ps, B], [t, x, y, z])
kx = k * sp.sqrt(1 - mu ** 2); kz = k * mu; w = kz * v
ph_, ps_, B_, rb_, rp_ = sp.symbols("ph_ ps_ B_ rb_ rp_")
E = sp.exp(sp.I * (kx * x + kz * z - w * t))
sub = {ph: ph_ * E, ps: ps_ * E, B: B_ * E, rb: rb_ * E, rp: rp_ * E}
lin = [sp.simplify((e.lhs.subs(sub).doit()) / E) for e in eqs]
sol = sp.solve(lin, [ph_, ps_, B_], dict=True)[0]
phs = sp.simplify(sol[ph_].subs(rb_, 0))
ph0 = sp.simplify(sp.limit(phs, v, 0))
R.check("G7.1 static limit: phi = -4 pi G rho / (k^2 (1 - c14/2)) i.e. G_N = G/(1 - c14/2) (matches the record's static block; own derivation)",
        str(ph0), sp.simplify(ph0 + 4 * sp.pi * Gs * rp_ / (k ** 2 * (1 - c14 / 2))) == 0)
ser = sp.series(phs / ph0, v, 0, 3).removeO()
Cme = sp.factor(sp.simplify(ser.coeff(v, 2) / mu ** 2))
Phiph = -4 * sp.pi * Gs * rp_ / k ** 2
Cabs = sp.factor(sp.simplify(ser.coeff(v, 2) * ph0 / mu ** 2 / Phiph))
C_rec = (4 + 4 * c2 + c14 * c2) / (c2 * (2 - c14))                   # the record's C_ph (L333 R2), used ONLY as control
R.out["numbers"]["C_derived_ratio_to_static"] = str(Cme)
R.out["numbers"]["C_derived_relative_to_Phi_ph"] = str(Cabs)
R.check("G7.2 derived: phi = phi_static (1 + C v^2 mu^2), C = 2(2+3c2)/(c2(2-c14)) (moving momentumless lapse source; own solve)", str(Cme),
        sp.simplify(Cme - 2 * (2 + 3 * c2) / (c2 * (2 - c14))) == 0)
lead = sp.limit(Cme / C_rec, c2, 0)
R.check("C3 the record's leading behaviour C ~ 4/(c2 (2 - c14)) is reproduced (ratio derived/record -> 1 as c2 -> 0); the O(c2) terms DIFFER (derived 6 c2, record 4 c2 + c14 c2): kept, immaterial at c2 <= 1e-3 for G7",
        f"limit ratio = {lead}", lead == 1)
# deep-MOND profile: radial and tilt distortion
r_, C_, V_ = sp.symbols("r C V", positive=True)
th = sp.symbols("theta")
Ff = V_ ** 2 * (r_ ** 2 * sp.log(r_) / 6 - sp.Rational(5, 36) * r_ ** 2)     # lap^{-1} of V^2 ln r
X_, Y_, Z_ = sp.symbols("X Y Z", positive=True)
rr3 = sp.sqrt(X_ ** 2 + Y_ ** 2 + Z_ ** 2)
Fc = Ff.subs(r_, rr3)
dn = C_ * sp.diff(Fc, Z_, 2)                                                      # delta n = C v^2 (vhat . grad)^2 lap^-1 Phi_ph (v^2 absorbed in C_)
dn_sph = sp.simplify(dn.subs({X_: r_ * sp.sin(th), Y_: 0, Z_: r_ * sp.cos(th)}))
d_r = sp.simplify(sp.diff(dn_sph, r_)); d_th = sp.simplify(sp.diff(dn_sph, th) / r_)
gph = V_ ** 2 / r_
rad = sp.simplify(d_r / gph); til = sp.simplify(d_th / gph)
R.check("G7.3 deep-MOND phantom (g = V^2/r): radial input distortion = C v^2/3 isotropic, tilt = (C v^2/3) sin 2 theta (own sympy; matches the record's D/3 structure)",
        f"radial/g = {rad}, tilt/g = {til}", sp.simplify(rad - C_ / 3) == 0 and sp.simplify(til + C_ * sp.sin(2 * th) / 3) == 0)
# FRW minisuperspace check of G_cos/G_N (L350's formula)
a_, N_, H_ = sp.symbols("a N H", positive=True)
adot = sp.Symbol("adot")
rho_, Lam = sp.symbols("rho Lambda")
Lm = a_ ** 3 * N_ * (-6 * (1 + sp.Rational(3, 2) * c2) * (adot / (a_ * N_)) ** 2 - 2 * Lam) / (16 * sp.pi * Gs) - a_ ** 3 * N_ * rho_
Fr = sp.simplify(sp.diff(Lm, N_).subs(N_, 1).subs(adot, H_ * a_))
Gc = sp.simplify(sp.solve(sp.Eq(Fr, 0), H_ ** 2)[0])
R.check("C4 FRW minisuperspace: H^2 (1 + 3 c2/2) = 8 pi G rho/3 + Lambda/3, so G_cos = G/(1 + 3c2/2) (L350 formula, own derivation); with G_N = G/(1 - c14/2): G_cos/G_N = (2-c14)/(2+3c2)",
        str(Gc), sp.simplify(Gc - (8 * sp.pi * Gs * rho_ / 3 + Lam / 3 * 0 - 0) / (1 + sp.Rational(3, 2) * c2) + Lam / (3 * (1 + sp.Rational(3, 2) * c2)) * 0) is not None and sp.simplify(Gc * (1 + sp.Rational(3, 2) * c2) - (8 * sp.pi * Gs * rho_ / 3 + Lam / 3)) == 0)

# ---- G7 numbers -------------------------------------------------------------------------------------------------------------
Cf = sp.lambdify((c2, c14), Cme, "numpy")
def dev_iso(c2v, c14v, wk=W_KMS):
    return float(Cf(c2v, c14v)) * (wk / C_KMS) ** 2 / 3.0
# record numbers as control (leading behaviour), 620 km/s
R.check("C3b D/3 at 620 km/s: 0.114 (c2 = 2.5e-5) and 0.285 (c2 = 1e-5), from the derived C at c14 = 1e-5", f"{dev_iso(2.5e-5,1e-5,620):.3f}, {dev_iso(1e-5,1e-5,620):.3f}",
        abs(dev_iso(2.5e-5, 1e-5, 620) - 0.114) < 0.005 and abs(dev_iso(1e-5, 1e-5, 620) - 0.285) < 0.01)
# minimum c2 for D/3 <= 0.10 at w, for c14_eff = 0 and 1 (MOND-regime dressing)
def c2_min(c14v, wk, tol=0.10):
    return brentq(lambda lc: dev_iso(10 ** lc, c14v, wk) - tol, -14, 2, xtol=1e-12)
c2min = {c14v: 10 ** c2_min(c14v, W_KMS) for c14v in (0.0, 1e-3, 0.5, 1.0)}
c2min_600 = {c14v: 10 ** c2_min(c14v, 600.0) for c14v in (0.0, 1e-3, 0.5, 1.0)}
P("  smallest c2 with D/3 <= 0.10 at w=%g km/s, by the effective c14 of the a-channel:" % W_KMS, {k_: f"{v_:.2e}" for k_, v_ in c2min.items()})
R.out["numbers"]["c2_min_G7"] = {"w_kms": W_KMS, **{str(k_): v_ for k_, v_ in c2min.items()}}
R.out["numbers"]["c2_min_G7_at_600"] = {str(k_): v_ for k_, v_ in c2min_600.items()}
# 11C-a / -c at a window value of c2 (declared representative 5e-4, inside [c2min(c14=1), Planck ceiling 6.3e-4])
c2_rep = 5e-4
G7a = max(dev_iso(c2_rep, c14v) for c14v in (0.0, 0.5, 1.0))
G7a_pass = G7a <= 0.10
P(f"  11C-a/-c at c2 = {c2_rep:g}: worst D/3 over c14_eff in {{0, .5, 1}} = {G7a:.3f} at w = {W_KMS:g} km/s")
R.verdict("G7 (11C-a, -c) in the KM1 modelling at c2 = 5e-4", "PASS" if G7a_pass else "FAIL",
          f"D/3 = {G7a:.3f}; pass iff c2 >= {c2min_600[1.0]:.2e} (c14_eff = 1) .. {c2min_600[0.0]:.2e} (c14_eff = 0) at 600 km/s; the transfer to the nonlinear a^2-channel is not derived (phantom modelled as a momentumless lapse source with the linear-theory c14) => overall status UNDEFINED")

# ---- G6 ----------------------------------------------------------------------------------------------------------------------
def alpha1(c14v): return -4.0 * c14v
def alpha2(c14v, c2v): return c14v * (c14v - c2v + 2 * c14v * c2v) / (c2v * (2 - c14v))
LIM1 = {"frozen 3.4e-5": 3.4e-5, "data-chat 3.5e-5": 3.5e-5, "Liu+2020 2.1e-5 (strong field, CMB frame; from the data-chat note)": 2.1e-5}
LIM2 = 1.6e-9
def q_P2(yv): return 1.0 - (math.sqrt(1 + 4 * yv * yv) - 1) / (2 * yv) if yv < 1e6 else 1.0 / (2 * yv) - 1.0 / (8 * yv ** 3)
# a / c: local effective c14 = q(y) at the test system's own acceleration
GMS = 1.32712440018e20; AU = 1.495978707e11
tests = {"Earth orbit (1 AU)": GMS / AU ** 2, "Saturn (9.54 AU)": GMS / (9.537 * AU) ** 2, "binary-pulsar orbit (hand: 73 m/s^2, from memory)": 73.0}
g6a = {}
for nm, gacc in tests.items():
    for f in FOOT:
        qv = q_P2(gacc / A0_SI[f])
        a1 = alpha1(qv); a2 = alpha2(qv, c2_rep)
        g6a[f"{nm}/{f}"] = {"q": qv, "alpha1": a1, "alpha2": a2}
        P(f"  G6 (a,c; c2={c2_rep:g}) {nm:52s} {f:9s}: q={qv:.2e}  alpha1={a1:.2e}  alpha2={a2:.2e}")
sol_sys = [v_ for k_, v_ in g6a.items() if "pulsar" not in k_]
pul = [v_ for k_, v_ in g6a.items() if "pulsar" in k_]
g6a_ok = {nm: all(abs(v_["alpha1"]) <= lim for v_ in sol_sys) for nm, lim in LIM1.items()}
g6a_ok2 = all(abs(v_["alpha2"]) <= LIM2 for v_ in pul)
R.out["numbers"]["G6_ac"] = g6a
R.verdict("G6 (11C-a, -c), isolated systems at their own acceleration", "PASS" if (all(g6a_ok.values()) and g6a_ok2) else "FAIL",
          f"alpha1 within each line {g6a_ok} (the three lines agree: {len(set(g6a_ok.values()))==1}); alpha2(pulsar) within 1.6e-9: {g6a_ok2}; quoted formulas, not re-derived")
P("  NOTE: alpha2 = %.1e at Saturn / %.1e at 1 AU would exceed 1.6e-9 if the strong-field pulsar limit were applied to planetary-scale systems; the limit is a strong-field one (data-chat note), so it is applied to the pulsar row only." % (abs(g6a['Saturn (9.54 AU)/canonical']['alpha2']), abs(g6a['Earth orbit (1 AU)/canonical']['alpha2'])))
R.out["numbers"]["G6_alpha1_lines_agree_ac"] = len(set(g6a_ok.values())) == 1

# ---- NOT SCORED: the ambient-field reading (the v9-AeST PPN kill of the record evaluated the aether coefficients at the deep-field background) ----------------
g_gal = 1.055e-10 * (1 + 0.0)                       # MW Newtonian field at the Sun (CFG7 H1 budget, canonical), m/s^2
amb = {}
for f in FOOT:
    a0 = A0_SI[f]
    y_tot = float(nu_p2(g_gal / a0)) * g_gal / a0
    qv = q_P2(y_tot)
    amb[f] = {"y_gal_total": y_tot, "q": qv, "alpha1": alpha1(qv)}
    P(f"  [NOT SCORED] ambient reading, {f}: if the preferred-frame sector of the Solar System were set by the galactic background field (y = {y_tot:.2f}), q = {qv:.3f}, alpha1 = {alpha1(qv):.2f} (limit 3.4e-5): FAIL by {abs(alpha1(qv))/3.4e-5:.1e}")
R.out["numbers"]["G6_ambient_reading_not_scored"] = amb

# b: tie fixes c14 / c2 = 24 pi / kappa^2 (Lambda-tie) or 24 pi/(Omega_L kappa^2) (actual 3H0); scan c2
kap = 0.5
ratios = {"Lambda-tie (theta_Lambda)": 24 * math.pi / kap ** 2, "actual theta = 3H0": 24 * math.pi / (OL * kap ** 2)}
R.out["numbers"]["b_tie_ratios_c14_over_c2"] = ratios
c2s = np.logspace(-16, 0, 1601)
regionG6, regionG7 = {}, {}
for nm, rat in ratios.items():
    c14s = rat * c2s
    ok6 = np.array([(abs(alpha1(a_)) <= 3.4e-5) and (abs(alpha2(a_, b_)) <= LIM2) for a_, b_ in zip(c14s, c2s) if True])
    ok6b = np.array([(abs(alpha1(a_)) <= 3.5e-5) and (abs(alpha2(a_, b_)) <= LIM2) for a_, b_ in zip(c14s, c2s)])
    ok6c = np.array([(abs(alpha1(a_)) <= 2.1e-5) and (abs(alpha2(a_, b_)) <= LIM2) for a_, b_ in zip(c14s, c2s)])
    ok1_only = {ln: np.array([abs(alpha1(a_)) <= lm for a_ in c14s]) for ln, lm in (("3.4e-5", 3.4e-5), ("3.5e-5", 3.5e-5), ("2.1e-5", 2.1e-5))}
    c2_alpha1_ceiling = {ln: float(c2s[arr].max()) for ln, arr in ok1_only.items()}
    ok7 = np.array([dev_iso(b_, a_, W_KMS) <= 0.10 if a_ < 1.9 else False for a_, b_ in zip(c14s, c2s)])
    both = ok6 & ok7
    regionG6[nm] = {"c2_max_G6": float(c2s[ok6].max()) if ok6.any() else None, "c2_min_G7": float(c2s[ok7].min()) if ok7.any() else None,
                    "G6_G7_both_points": int(both.sum()), "G6_three_lines_same": bool(np.array_equal(ok6, ok6b) and np.array_equal(ok6, ok6c)), "c2_ceiling_from_alpha1_alone": c2_alpha1_ceiling}
    P(f"  11C-b tie [{nm}]: c14/c2 = {rat:.1f}; G6 allows c2 <= {regionG6[nm]['c2_max_G6']:.2e}; G7 needs c2 >= {regionG6[nm]['c2_min_G7']:.2e}; points passing both: {regionG6[nm]['G6_G7_both_points']}; the three alpha1 lines give the same G6 region: {regionG6[nm]['G6_three_lines_same']}; alpha1-alone ceilings on c2: {regionG6[nm]['c2_ceiling_from_alpha1_alone']}")
R.out["numbers"]["b_region"] = regionG6
b_none = all(v_["G6_G7_both_points"] == 0 for v_ in regionG6.values())
R.verdict("G6 x G7 (11C-b under rule T)", "FAIL" if b_none else "PASS", "no c2 satisfies |alpha_2| <= 1.6e-9 and D/3 <= 0.10 with the tie-fixed c14/c2" if b_none else "a point passes")
# the allowed set A = G6 and G7 in the (c2, c14) plane (untied) and its minimum t = 440 c2/c14 (input to A6)
cc2 = np.logspace(-10, -1, 400); cc14 = np.logspace(-14, -1, 400)
tmin = np.inf
for a_ in cc14:
    for b_ in cc2:
        if abs(alpha1(a_)) <= 3.4e-5 and abs(alpha2(a_, b_)) <= LIM2 and a_ < 1.9 and dev_iso(b_, a_, 600.0) <= 0.10:
            tmin = min(tmin, 24 * math.pi / (OL * kap ** 2) * b_ / a_)
R.out["numbers"]["t_min_in_G6G7_allowed_set"] = float(tmin)
P(f"  untied (c2, c14) plane: min over G6 and G7 allowed points of t = K_bg/K_0 = 440 c2/c14 -> {tmin:.3e}")
R.out["numbers"]["G6_lines"] = "3.4e-5, 3.5e-5, 2.1e-5: same verdict for every variant (see G6 lines above); alpha_2 <= 1.6e-9 is the binding line for 11C-b"
bite = (mut == "M5") and (not G7a_pass)
R.finish(bite=(mut != "" and bite))
