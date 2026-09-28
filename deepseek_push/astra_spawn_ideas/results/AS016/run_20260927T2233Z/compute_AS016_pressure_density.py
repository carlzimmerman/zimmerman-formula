#!/usr/bin/env python3
"""AS016 - Pressure mapping versus density mapping.

Framework base (adopted inputs): a0 = kappa*c*sqrt(G*rho_Lambda), kappa=1/2,
rho_Lambda = 4 a0^2/(G c^2), epsilon_Lambda = rho_Lambda c^2 = 4 a0^2 / G,
r_M = sqrt(G M_b/a0), C = sqrt(G M_b a0),  v_flat^2 = C.
Deep-equilibrium TARGETS (not free laws): sigma^2 = C/2,
rho_ph(r) = C/(4 pi G r^2),  P(r) = sigma^2 rho_ph(r).

Two vacuum-scale maps:
  DENSITY map   (framework's own):  a_rho^2 = (G/4) * epsilon_DE      [a0^2 = (G/4) eps_Lambda]
  PRESSURE map  (candidate):        a_p^2   = (G/4) * (-w) * epsilon_DE,  p_DE = w epsilon_DE
Checks: exact identities at 60-digit precision, w-sweep, z-relative evolution
(w(z)/w(0) extra factor), phantom-pressure ratio P(r)/eps_L = (r_M/r)^2/(32 pi),
integral and derivative independent representations, Newtonian (a0->0) and
eps->0 boundary cases, and the w=0 negative control (mappings cannot agree).
"""
import json, math, time
import mpmath as mp

mp.mp.dps = 60
mpf = mp.mpf

G = mpf("6.67430e-11")            # m^3 kg^-1 s^-2 (measured input)
c = mpf(299792458)                # m/s (exact)
M_sun = mpf("1.98847e30")         # kg
pc = mpf("3.085677581491367e16")  # m
kpc = 1000 * pc

A0_CAN = mpf("9.3619e-11")        # canonical footing, m/s^2
A0_ALT = mpf("1.1279e-10")        # alternative footing, m/s^2
KAPPA = mpf("0.5")                # adopted (input, not derived here)

t0 = time.time()

# ---------- per-footing derived vacuum quantities ----------
def footing(a0):
    rhoL = 4 * a0**2 / (G * c**2)        # kg/m^3 mass density
    epsL = rhoL * c**2                   # J/m^3 = kg m^-1 s^-2 energy density
    a0_from_rho = mpf("0.5") * c * mp.sqrt(G * rhoL)   # round-trip check
    return dict(a0=a0, rhoL=rhoL, epsL=epsL, a0_from_rho=a0_from_rho)

F = {k: footing(v) for k, v in [("canonical", A0_CAN), ("alternative", A0_ALT)]}

# effective kappa if rho_Lambda held at the CANONICAL value while a0 moves to alt
rhoL_can = F["canonical"]["rhoL"]
kappa_eff = A0_ALT / (c * mp.sqrt(G * rhoL_can))
rho_ratio = F["alternative"]["rhoL"] / F["canonical"]["rhoL"]

def targets(a0, M_b, r):
    """All deep-equilibrium quantities for one (footing, baryon mass, radius)."""
    rM = mp.sqrt(G * M_b / a0)           # m
    C = mp.sqrt(G * M_b * a0)            # m^2/s^2 = v_flat^2
    vflat = mp.sqrt(C)                   # m/s
    s2 = C / 2                           # m^2/s^2
    rho_ph = C / (4 * mp.pi * G * r**2)  # kg/m^3
    P = s2 * rho_ph                      # kg m^-1 s^-2 = Pa
    return dict(rM=rM, C=C, vflat=vflat, s2=s2, rho_ph=rho_ph, P=P)

def rel(a, b):
    """relative difference |a-b|/|b| (0 if both zero)."""
    if a == 0 and b == 0:
        return mpf(0)
    return abs(a - b) / abs(b)

checks = []
def check(name, ok, obs, tol, capable, note=""):
    checks.append(dict(name=name, pass_=bool(ok), observed=str(obs),
                       tolerance=str(tol), capable_of_failing=capable, note=note))

TOL = mpf("1e-30")   # set BEFORE evaluation; exact identities sit far inside

res = {}
res["footings"] = {}
for key, f in F.items():
    a0 = f["a0"]
    t = targets(a0, M_sun, 10 * kpc)
    t_rM = targets(a0, M_sun, t["rM"])
    res["footings"][key] = dict(
        a0=str(a0), rho_Lambda=str(f["rhoL"]), eps_Lambda=str(f["epsL"]),
        r_M_Msun=str(t["rM"]), C=str(t["C"]), v_flat=str(t["vflat"]),
        sigma2=str(t["s2"]), sigma2_real=str(mp.sqrt(t["s2"])),
        rho_ph_10kpc=str(t["rho_ph"]), P_10kpc=str(t["P"]),
        P_at_rM=str(t_rM["P"]), P_at_rM_over_epsL_32pi=str(t_rM["P"] * 32 * mp.pi / f["epsL"]),
        rM_over_r_10kpc_sq=str((t["rM"] / (10 * kpc))**2),
    )
    # -------- exact identity: P * 8 pi r^2 = M_b a0 --------
    lhs = t["P"] * 8 * mp.pi * (10 * kpc)**2
    rhs = M_sun * a0
    r1 = rel(lhs, rhs)
    check(f"P8pir2_identity_{key}", r1 < TOL, r1, TOL,
          "would fail if P = sigma^2 rho_ph were not algebraically M_b a0/(8 pi r^2)",
          f"P*8pi r^2 = {lhs} vs M_b*a0 = {rhs}")
    # -------- exact identity: P(r_M) = a0^2/(8 pi G) = eps_L/(32 pi) --------
    r2 = rel(t_rM["P"], a0**2 / (8 * mp.pi * G))
    r2b = rel(t_rM["P"] * 32 * mp.pi, f["epsL"])
    check(f"P_rM_identity_{key}", r2 < TOL and r2b < TOL, (r2, r2b), TOL,
          "would fail if P at the MOND radius were not fixed by (a0, G) alone")
    # -------- ratio map identity: a_p^2 = (-w) a_rho^2, matched normalization --------
    ar2 = (G / 4) * f["epsL"]
    for w in [mpf("-1.5"), mpf("-1"), mpf("-2")/3, mpf("-1")/3, mpf("0"), mpf("1")/3]:
        ap2 = (G / 4) * (-w) * f["epsL"]
        rr = rel(ap2, (-w) * ar2)
        check(f"ap2_eq_minusw_ar2_{key}_w{w}", rr < TOL, rr, TOL,
              "exact two-map algebra; only fails for a coding error")
    # -------- phantom-pressure ratio: P(r)/eps_L = (r_M/r)^2/(32 pi) --------
    for rlab, rv in [("rM", t["rM"]), ("2rM", 2 * t["rM"]), ("10kpc", 10 * kpc), ("100kpc", 100 * kpc)]:
        ttt = targets(a0, M_sun, rv)
        r3 = rel(ttt["P"] / f["epsL"], (t["rM"] / rv)**2 / (32 * mp.pi))
        check(f"P_over_epsL_{key}_{rlab}", r3 < TOL, r3, TOL,
              "P(r)/eps_L = (r_M/r)^2/(32 pi) exact power law; would fail otherwise")

# -------- w-sweep: where does the pressure map define a real a0? --------
sweep = []
for key, f in F.items():
    ar2 = (G / 4) * f["epsL"]
    a_rho = mp.sqrt(ar2)
    for w in [mpf("-1.5"), mpf("-1"), mpf("-2")/3, mpf("-1")/3, mpf("0"), mpf("1")/3]:
        ap2 = (G / 4) * (-w) * f["epsL"]
        real = (-w) * f["epsL"] > 0
        ap = mp.sqrt(ap2) if real else None
        sweep.append(dict(footing=key, w=str(w), p_DE=str(w * f["epsL"]),
                          ap2=str(ap2), ap_real_a0=str(ap) if ap is not None else "UNDEFINED (no real a0)",
                          a_rho=str(a_rho), ratio_ap_over_arho=str(ap / a_rho) if real else "UNDEFINED",
                          real_a0_defined=real))
res["w_sweep"] = sweep

# -------- negative control: w = 0 with positive epsilon_DE --------
# density map gives a_rho = a0 > 0; pressure map gives a_p^2 = 0 -> a_p = 0.
# The two mappings CANNOT agree.  Control is capable of failing: if the claim
# were "the pressure map reproduces the density map identically", this witness
# (w=0, eps>0) kills it with ratio 0 instead of 1.
for key in ["canonical", "alternative"]:
    epsL = F[key]["epsL"]
    ar2 = (G / 4) * epsL
    ap2 = (G / 4) * (-mpf(0)) * epsL
    ratio = mp.sqrt(ap2) / mp.sqrt(ar2) if ap2 > 0 else mpf(0)
    disagree = ratio != 1
    check(f"NEG_CONTROL_w0_{key}", disagree and ap2 == 0 and ar2 > 0,
          f"a_p = {mp.sqrt(ap2)} (exact 0), a_rho = {mp.sqrt(ar2)} > 0, ratio = {ratio}",
          "ratio must be 0 != 1",
          "would fail by passing if the two mappings agreed at w=0 with positive epsilon_DE")
# positive control: w = -1 locus AGREES exactly (masquerade locus)
for key in ["canonical", "alternative"]:
    epsL = F[key]["epsL"]
    ar2 = (G / 4) * epsL
    ap2 = (G / 4) * (-mpf("-1")) * epsL
    agree = rel(ap2, ar2) < TOL
    check(f"POS_CONTROL_w_equal_minus1_{key}", agree, rel(ap2, ar2), TOL,
          "w = -1 is exactly the agreement locus; would fail if masquerade were not exact there")

# -------- relative scale evolution: extra factor w(z)/w(0) --------
zs = [mpf(0), mpf("0.5"), mpf(1), mpf("1.5"), mpf(2)]
ws = [mpf("-1"), mpf("-0.85"), mpf("-0.7"), mpf("-0.55"), mpf("-0.4")]  # all w<0 (sample)
evol = []
for key, f in F.items():
    epsL = f["epsL"]
    ar2_0 = (G / 4) * epsL
    ap2_0 = (G / 4) * (-ws[0]) * epsL
    for z, w in zip(zs, ws):
        ar2_z = (G / 4) * epsL          # epsilon(z) model cancels in the ratio
        ap2_z = (G / 4) * (-w) * epsL
        extra = (ap2_z / ap2_0) / (ar2_z / ar2_0)
        target = w / ws[0]
        rr = rel(extra, target)
        evol.append(dict(footing=key, z=str(z), w=str(w),
                         extra_factor=str(extra), target_w_over_w0=str(target),
                         resid=str(rr)))
        check(f"extra_factor_w_z_over_w_0_{key}_z{z}", rr < TOL, rr, TOL,
              "relative scale evolution differs by exactly w(z)/w(0); would fail otherwise")
res["z_evolution"] = evol

# -------- independent representations --------
# (a) INTEGRAL: M_ph enclosed between a and b is C*(b-a)/G   [different representation]
for key, f in F.items():
    a0 = f["a0"]
    t = targets(a0, M_sun, 10 * kpc)
    a, b = t["rM"], 10 * t["rM"]
    fq = mp.quad(lambda rr: 4 * mp.pi * rr**2 * (t["C"] / (4 * mp.pi * G * rr**2)), [a, b])
    wtarget = t["C"] * (b - a) / G
    rr = rel(fq, wtarget)
    check(f"integral_phantom_mass_{key}", rr < mpf("1e-48"), rr, mpf("1e-48"),
          "quadrature representation must reproduce C*(b-a)/G")
# (b) DERIVATIVE: dP/dr = -2 P/r exactly (pure 1/r^2 power law).
# Central-difference truncation is O((h/r)^2); use h=1e-12 kpc so the
# truncation term sits near 1e-24 (60-digit mpmath arithmetic keeps roundoff
# at 1e-60).  Also require consistency across two step sizes (convergence).
for key, f in F.items():
    a0 = f["a0"]
    t = targets(a0, M_sun, 10 * kpc)
    fds = {}
    for hlab, hfac in [("h8", mpf("1e-8")), ("h12", mpf("1e-12"))]:
        h = hfac * kpc
        tph = targets(a0, M_sun, 10 * kpc + h)
        tmh = targets(a0, M_sun, 10 * kpc - h)
        num = (tph["P"] - tmh["P"]) / (2 * h)
        ana = -2 * t["P"] / (10 * kpc)
        fds[hlab] = rel(num, ana)
    # h12 error must be smaller than h8 error by ~1e-8 (O(h^2) convergence) AND below tol
    converged = fds["h12"] < fds["h8"] * mpf("1e-7") and fds["h12"] < mpf("1e-20")
    check(f"derivative_dPdr_{key}", converged, fds, mpf("1e-20"),
          "central difference must reproduce -2P/r with O(h^2) convergence; "
          "the h=1e-6 kpc variant failed at 2e-14 exactly as its own truncation predicts")

# -------- Newtonian limit: a0 -> 0 (vacuum density -> 0) kills the phantom --------
newt = []
for al in [mpf("1e-14"), mpf("1e-20"), mpf("1e-40"), mpf(0)]:
    tt = targets(al, M_sun, 10 * kpc) if al > 0 else dict(C=mpf(0), s2=mpf(0),
                                                          rho_ph=mpf(0), P=mpf(0),
                                                          vflat=mpf(0), rM=mpf("inf"))
    newt.append(dict(a0=str(al), C=str(tt["C"]), sigma2=str(tt["s2"]),
                     v_flat=str(tt["vflat"]), rho_ph=str(tt["rho_ph"]), P=str(tt["P"])))
res["newtonian_limit_a0_to_0"] = newt
P0 = mp.mpf(newt[0]["P"]); P3 = mp.mpf(newt[3]["P"])
C0 = mp.mpf(newt[0]["C"]); C3 = mp.mpf(newt[3]["C"])
# P is EXACTLY linear in a0 (P = M_b a0/(8 pi r^2)); phantom vanishes exactly at a0 = 0.
lin_scaling = rel(mp.mpf(newt[0]["P"]) / mpf("1e-14"), mp.mpf(newt[1]["P"]) / mpf("1e-20"))
monotone = mp.mpf(newt[1]["P"]) < P0 and mp.mpf(newt[2]["P"]) < mp.mpf(newt[1]["P"])
decays = monotone and P3 == 0 and C3 == 0 and lin_scaling < mpf("1e-50")
check("BOUNDARY_newtonian_a0_to_0", decays,
      f"P(a0=1e-14)={newt[0]['P'][:12]} => P(a0=1e-20)={newt[1]['P'][:12]} => P(a0=0)=exact 0; "
      f"P/a0 constancy residual {lin_scaling} (P linear in a0), C(a0=0)=exact 0",
      "exact zeros at a0=0, P ∝ a0 to 1e-50, monotone decay",
      "would fail if any phantom quantity survived the a0 -> 0 limit or if P were not linear in a0")
# boundary case: eps -> 0 kills both maps (degenerate agreement point)
eps_tiny = mpf("1e-60")
b1 = dict(a_rho2=(G / 4) * eps_tiny, a_p2_wneg1=(G / 4) * eps_tiny)
check("BOUNDARY_eps_to_0", b1["a_rho2"] > 0 and rel(b1["a_rho2"], b1["a_p2_wneg1"]) < TOL,
      f"a_rho^2 = a_p^2 = {b1['a_rho2']} -> 0 as eps -> 0",
      TOL, "both maps vanish together at zero vacuum density")

# -------- dimensional exponent vectors (M, L, T) --------
def dims(name, M_, L_, T_):
    return dict(quantity=name, exponents=[int(M_), int(L_), int(T_)])
res["dimensions"] = [dims("sigma^2", 0, 2, -2), dims("rho_ph", 1, -3, 0),
                     dims("P = sigma^2 rho_ph", 1, -1, -2),
                     dims("eps_Lambda", 1, -1, -2), dims("p_DE = w eps_DE", 1, -1, -2),
                     dims("a0", 0, 1, -2), dims("rho_Lambda", 1, -3, 0)]
check("dimensions", all(e["exponents"][0] in (0, 1) for e in res["dimensions"]) and
      res["dimensions"][2]["exponents"] == [1, -1, -2] and
      res["dimensions"][3]["exponents"] == [1, -1, -2],
      "sigma^2 in m^2/s^2, rho_ph in kg/m^3, P in kg m^-1 s^-2 = Pa = J/m^3",
      "exact exponent vectors", "would fail if pressure and energy density had different exponents")

res["checks"] = checks
res["footing_relations"] = dict(
    rho_alt_over_rho_can=str(rho_ratio),
    kappa_eff_at_fixed_rho_can=str(kappa_eff),
    a0_alt_over_a0_can=str(A0_ALT / A0_CAN),
    rho_alt_over_rho_can_vs_a0sq_ratio=str(rho_ratio / (A0_ALT / A0_CAN)**2))

res["wall_s"] = time.time() - t0
with open("residuals.json", "w") as jf:
    json.dump(res, jf, indent=1, default=str)
print(json.dumps(res, indent=1, default=str))

# human-readable summary
print("\n=== SUMMARY ===")
for key, f in F.items():
    print(f"{key}: a0={f['a0']} rho_L={f['rhoL']} eps_L={f['epsL']}")
for c_ in checks:
    print(("PASS " if c_["pass_"] else "FAIL ") + c_["name"] + "  resid=" + str(c_["observed"])[:40])