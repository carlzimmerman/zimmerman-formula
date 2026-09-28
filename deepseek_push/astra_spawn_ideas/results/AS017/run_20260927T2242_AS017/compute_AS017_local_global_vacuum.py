#!/usr/bin/env python3
"""
AS017 — Local versus global vacuum input: premise audit.

Whether rho_Lambda entering a0 = kappa*c*sqrt(G*rho_Lambda) is a global
cosmological constant or a locally varying density (a0(x)^2 = kappa^2*G*eps_L(x)),
and what each implies for EFE, clusters, and RAR scatter.

Bounded prototype: single-threaded, 801-point grid, no refinement loop.
All identities dimensionless; both footings carried on every dimensional number.
"""
import json, math, time, resource, os

t_start = time.time()
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

# ---------------------------------------------------------------- constants
G   = 6.67430e-11        # m^3 kg^-1 s^-2  (framework input)
c   = 299792458.0        # m/s
M_sun = 1.98847e30       # kg
pc  = 3.085677581491367e16  # m
kappa  = 0.5             # ADOPTED (fitted, not derived)
A0_CAN = 9.3619e-11      # m/s^2 canonical footing
A0_ALT = 1.1279e-10      # m/s^2 alternative footing

def eps_of_a0(a0):
    """vacuum energy density eps [J/m^3] implied by a0^2 = kappa^2 G eps."""
    return a0 * a0 / (kappa * kappa * G)

def rho_of_a0(a0):
    return eps_of_a0(a0) / c**2

EPS_CAN, RHO_CAN = eps_of_a0(A0_CAN), rho_of_a0(A0_CAN)
EPS_ALT, RHO_ALT = eps_of_a0(A0_ALT), rho_of_a0(A0_ALT)

# ---------------------------------------------------------------- kernels
def nu_RAR(y):
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))

def dnu_RAR(y):
    s = math.sqrt(y)
    return -math.exp(-s) / (2.0 * s * (1.0 - math.exp(-s))**2)

# ---------------------------------------------------------------- C1: transfer identity
def check_C1():
    """delta a0/a0 = delta eps/(2 eps): exact finite form (sqrt(1+q)-1) = q/(1+sqrt(1+q))."""
    out = {"q": [], "exact_finite": [], "linear_1half": [], "resid_finite": [], "resid_linear": []}
    for q in (-0.5, -0.1, -0.01, 0.01, 0.1, 0.5):
        for a0 in (A0_CAN, A0_ALT):
            e  = eps_of_a0(a0)
            a1 = math.sqrt(kappa*kappa*G*(e*(1.0+q)))
            ra = (a1 - a0)/a0
            out["q"].append(q)
            out["exact_finite"].append(ra)
            out["linear_1half"].append(0.5*q)
            out["resid_finite"].append(ra - q/(1.0+math.sqrt(1.0+q)))
            out["resid_linear"].append(ra - 0.5*q)
    return out

# ---------------------------------------------------------------- C2/C3: gradient terms, negative control
NGRID = 801
RLO, RHI = 0.01, 100.0          # in units of r_M
M_b = 1.0e11 * M_sun            # representative baryon mass (only sets the r scale)
r_M = math.sqrt(G*M_b/A0_CAN)

def make_a0_profile(delta, Ldec=1.0, a0base=A0_CAN):
    """smooth, bounded, nonzero-gradient vacuum-scale field
    a0(r) = a0base*(1 + delta*cos(2*pi*log10(r/r_M)/Ldec))  (period Ldec decades in log r)."""
    return lambda r: a0base * (1.0 + delta*math.cos(2.0*math.pi*math.log10(r/r_M)/Ldec))

def dln_a0_dr(r, a0f, h=None):
    if h is None:
        h = 1e-4 * r          # adaptive 5-pt step (r > 0 on grid)
    return ((a0f(r-2*h) - 8*a0f(r-h) + 8*a0f(r+h) - a0f(r+2*h)) / (12*h)) / a0f(r)

def grid_rs():
    return [r_M * 10**(math.log10(RLO) + (math.log10(RHI)-math.log10(RLO))*i/(NGRID-1))
            for i in range(NGRID)]

def check_C2C3(delta, Ldec=1.0):
    """S_ph = div[(nu(y(x))-1) grad w], w = G M_b / r (point baryon), y = |grad w|/a0(x).
    Full chain rule:  S = (nu-1) lap w + (nu'/a0)(grad w . grad|grad w|) - y nu' |grad w| (nhat . grad ln a0).
    Control: omitting the a0-gradient (treating a0 as constant inside the derivative)
    misses exactly Delta = - y nu' |grad w| (nhat . grad ln a0)."""
    a0f = make_a0_profile(delta, Ldec)
    rs = grid_rs()
    res = {"n": NGRID, "delta": delta, "Ldec": Ldec,
           "max_rel_resid_decomp": 0.0, "max_rel_resid_FD": 0.0,
           "max_abs_Delta_over_Sfull": 0.0,
           "sample_MOND": None, "sample_Newt": None}
    maxrd = 0.0; maxrF = 0.0; maxDD = 0.0
    for i in range(2, NGRID-2):
        r  = rs[i]
        gN = G*M_b/(r*r)
        a0 = a0f(r)
        y  = gN/a0
        nu = nu_RAR(y); dnu = dnu_RAR(y)
        # spherical point mass: lap w = 0 ; grad w . grad|grad w| = -2 gN^2 / r
        S_const = (dnu/a0)*(-2.0*gN*gN/r)          # a0 held constant inside the divergence
        Delta   = -y*dnu*gN*(dln_a0_dr(r, a0f))    # missing a0-gradient term
        S_full  = S_const + Delta
        # independent representation: 5-pt finite difference of V(r) = (nu(y(r))-1)*gN(r)
        hlr = (math.log(rs[1])-math.log(rs[0]))
        def Vln(l):
            rr = math.exp(l); aa = a0f(rr); yy = G*M_b/(rr*rr)/aa
            return (nu_RAR(yy)-1.0)
        lr = math.log(r)
        dVdr = (Vln(lr-2*hlr) - 8*Vln(lr-hlr) + 8*Vln(lr+hlr) - Vln(lr+2*hlr)) / (12*hlr) / r
        S_FD = gN*dVdr                                # (1/r^2) d[r^2 (nu-1) gN]/dr = gN d(nu-1)/dr
        # metrics restricted to the MOND regime (y <= 100, |S| not sub-float-noise):
        # the Newtonian tail (nu-1 ~ e^-sqrt(y) -> 1e-41) is reported separately below.
        if 1e-4 <= y <= 100.0 and abs(S_full) > 1e-30:
            maxrd = max(maxrd, abs(S_full - (S_const+Delta))/abs(S_full))
            maxrF = max(maxrF, abs(S_FD - S_full)/abs(S_full))
            maxDD = max(maxDD, abs(Delta)/abs(S_full))
        if y > 0.5 and y < 2.0 and res["sample_MOND"] is None:
            res["sample_MOND"] = {"r_rM": r/r_M, "y": y, "S_const": S_const,
                                  "Delta": Delta, "S_full": S_full, "S_FD": S_FD,
                                  "ratio_Delta_Sfull": Delta/S_full}
        if y > 1e3 and res["sample_Newt"] is None:
            res["sample_Newt"] = {"r_rM": r/r_M, "y": y, "S_const": S_const,
                                  "Delta": Delta, "S_full": S_full, "S_FD": S_FD,
                                  "ratio_Delta_Sfull": (Delta/S_full if S_full != 0 else 0.0),
                                  "note": "FD stencil underflows here (V ~ 1e-41); S_FD=0.0 excluded from FD metric"}
    res["max_rel_resid_decomp"] = maxrd
    res["max_rel_resid_FD"] = maxrF
    res["max_abs_Delta_over_Sfull"] = maxDD
    res["metric_domain"] = "y in [1e-4, 100], |S_full| > 1e-30"
    return res

def check_limits():
    """Missing term vanishes in the global limit (delta->0) and deep/Newtonian limits.
    Note: radii are chosen OFF the cosine profile's stationary points (log10(r/r_M) in 10^k
    gives sin(2 pi k) = 0); those would trivially give Delta ~ 0."""
    out = {}
    a0f = make_a0_profile(0.1)
    for tag, lx in (("deep_y1e-4", 1.9), ("mid_y1", 0.3), ("Newt_y1e2", -1.7),
                    ("Newt_y1e4", -1.95), ("stationary_sanity_y1", 0.0)):
        rp = r_M*10.0**lx
        gN = G*M_b/(rp*rp); a0 = a0f(rp); y = gN/a0
        dnu = dnu_RAR(y)
        S_const = (dnu/a0)*(-2.0*gN*gN/rp)
        Delta = -y*dnu*gN*dln_a0_dr(rp, a0f)
        out[tag] = {"log10_r_rM": lx, "y": y, "S_const": S_const,
                    "Delta": Delta, "S_full": S_const+Delta,
                    "|Delta|/|S_full|": abs(Delta)/abs(S_const+Delta) if S_const+Delta != 0 else float('nan'),
                    "dln_a0_dln_r": rp*dln_a0_dr(rp, a0f)}
    # global limit: delta -> 0 -> Delta -> 0 at the SAME non-stationary radius
    rp = r_M*10.0**0.3
    a0f0 = make_a0_profile(0.0)
    y = G*M_b/(rp*rp)/a0f0(rp); dnu = dnu_RAR(y)
    out["delta0_Delta_at_r10^0.3"] = -y*dnu*(G*M_b/(rp*rp))*(dln_a0_dr(rp, a0f0))
    return out

# ---------------------------------------------------------------- C4: deep-limit exact checks (local a0)
def check_deep(delta, Ldec=1.0):
    """Point baryon + spherically symmetric a0(r). Representations:
      R1  full RAR-QUMOND (unfiltered, spherical, exact): g = g_N * nu_RAR(g_N/a0(r))
      R2  deep closed form:                              g = sqrt(a0(r) g_N(r))
      exact relation: g_R1/g_R2 = t/(1-e^-t), t = sqrt(y)   (identity, checked to fp)
      leading term:   g_R1/g_R2 = 1 + t/2 + t^2/12 + ...     (behavioural -> 1 as y -> 0)
      Newtonian recovery (R1/g_N - 1 = e^-sqrt(y) -> 0) and flux constancy of R2 checked.
      transfer: d(g_rel)/d(deps/eps) -> 1/4 as y -> 0; residual is second order in delta;
      convergence in delta (0.1, 0.05, 0.025) verified at r = 10 r_M.
    """
    a0f = make_a0_profile(delta, Ldec)
    rs = grid_rs()
    out = {"delta": delta, "max_rel_flux_resid": 0.0,
           "max_dev_R1_R2_deep_domain": 0.0, "y_at_max_dev": None,
           "max_resid_exact_relation": 0.0,
           "lead_term_ratios": {}, "newtonian_tail": None,
           "transfer": {}}
    maxf = 0.0; maxdev = 0.0; ymax = 0.0; maxres = 0.0
    for i in range(1, NGRID):
        r = rs[i]; gN = G*M_b/(r*r); a0 = a0f(r)
        g2 = math.sqrt(a0*gN)                    # R2
        y = gN/a0
        g1 = gN*nu_RAR(y)                        # R1
        t = math.sqrt(y)
        flux = r*r*g2*g2/a0
        maxf = max(maxf, abs(flux - G*M_b)/(G*M_b))
        # exact relation g1/g2 = t/(1-e^-t) (fp identity)
        maxres = max(maxres, abs(g1/g2 - t/(1.0-math.exp(-t)))/(g1/g2))
        # deep-regime deviation of R2 vs R1 (domain: y <= 0.1, error ~ t/2)
        if y <= 0.1 and abs(g2) > 1e-300:
            dev = abs(g1/g2 - 1.0)
            if dev > maxdev:
                maxdev = dev; ymax = y
        if math.isclose(y, 0.001, rel_tol=0.3) or math.isclose(y, 0.01, rel_tol=0.3) \
           or math.isclose(y, 0.1, rel_tol=0.3):
            out["lead_term_ratios"][str(round(y, 4))] = (g1/g2 - 1.0)/(0.5*t)
        if y > 1e3 and out["newtonian_tail"] is None:
            out["newtonian_tail"] = {"y": y, "R1_over_gN_minus_1": g1/gN - 1.0,
                                     "e^{-sqrt y}": math.exp(-t)}
    out["max_rel_flux_resid"] = maxf
    out["max_dev_R1_R2_deep_domain"] = maxdev
    out["y_at_max_dev"] = ymax
    out["max_resid_exact_relation"] = maxres
    # transfer at r = 10 r_M with delta-refinement convergence (first-order coeff -> 1/4)
    r = 10.0*r_M
    gN = G*M_b/(r*r)
    for dlt in (0.1, 0.05, 0.025):
        af = make_a0_profile(dlt, Ldec)
        a0v = af(r); a0_0 = A0_CAN
        gv = gN*nu_RAR(gN/a0v); g0 = gN*nu_RAR(gN/a0_0)
        deps_eps = (eps_of_a0(a0v)-eps_of_a0(a0_0))/eps_of_a0(a0_0)
        yv = gN/a0v; y0 = gN/a0_0
        s_eff_mid = -0.5*(yv*dnu_RAR(yv)/nu_RAR(yv) + y0*dnu_RAR(y0)/nu_RAR(y0))
        meas = (gv-g0)/g0
        pred = s_eff_mid*0.5*deps_eps
        # second-order residual: for dlt -> 0 the ratio meas/pred -> 1
        out["transfer"][str(dlt)] = {
            "dlt": dlt, "y0": y0, "yv": yv, "deps_eps": deps_eps,
            "rel_diff_g_meas": meas, "first_order_pred": pred,
            "quarter_deps_eps": 0.25*deps_eps,
            "resid_vs_1st_order": meas - pred,
            "meas_over_pred_minus1": meas/pred - 1.0}
    return out

# ---------------------------------------------------------------- C6/C7: transfer tables (EFE, clusters, RAR scatter)
def transfer_tables():
    ys = [1e-4, 1e-3, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 100.0]
    rows = []
    for y in ys:
        s_RAR = -y*dnu_RAR(y)/nu_RAR(y)
        s_Q   = 1.0/(2.0*(1.0+y))
        rows.append({"y": y,
                     "s_RAR": s_RAR, "s_Q": s_Q,
                     "dlog10g_RAR_de0.1_dex": s_RAR*0.05/math.log(10.0),
                     "dlog10g_Q_de0.1_dex":   s_Q*0.05/math.log(10.0)})
    yD = (math.log(6.0/5.0))**2          # y at which D = nu = 6 (DERIVATIONS: median 5.998 at X-COP 300 kpc)
    sD = -yD*dnu_RAR(yD)/nu_RAR(yD)
    cluster = {"y_for_D6": yD, "D(yD)": nu_RAR(yD), "s_eff(yD)": sD,
               "DeltaD_over_D_de0.1": sD*0.05, "DeltaD_over_D_de0.3": sD*0.15}
    deep = {"dln_vflat_per_dln_eps": 0.25, "dln_rM_per_dln_eps": -0.25,
            "dln_g_per_dln_eps": 0.25, "dln_a0_per_dln_eps": 0.5}
    return {"rows": rows, "cluster": cluster, "deep": deep}

# ---------------------------------------------------------------- C8/C9: footings audit
def footings():
    a0_alt_eff_kappa = A0_ALT/math.sqrt(G*EPS_CAN)
    return {"eps_can_Jpm3": EPS_CAN, "rho_can_kgpm3": RHO_CAN,
            "eps_alt_Jpm3": EPS_ALT, "rho_alt_kgpm3": RHO_ALT,
            "kappa_eff_if_eps_canonical_and_a0_alt": a0_alt_eff_kappa,
            "kappa_eff_vs_half_rel": (a0_alt_eff_kappa-0.5)/0.5,
            "crosscheck_rho_can_vs_AS006_5.8444e-27_reldiff": abs(RHO_CAN-5.8444e-27)/5.8444e-27,
            "crosscheck_rho_alt_vs_AS006_8.4831e-27_reldiff": abs(RHO_ALT-8.4831e-27)/8.4831e-27}

# ---------------------------------------------------------------- run
results = {}
results["constants"] = {"G": G, "c": c, "M_sun": M_sun, "pc": pc, "kappa_adopted": kappa,
                        "a0_canonical": A0_CAN, "a0_alternative": A0_ALT,
                        "rM_Mb1e11Msun_canonical_m": r_M}
results["C1_transfer_identity"] = check_C1()
results["C2C3_gradient_decomp_delta0p1"] = check_C2C3(0.1)
results["C2C3_gradient_decomp_delta0"] = check_C2C3(0.0)
results["limits"] = check_limits()
results["C4_deep_checks"] = {"delta0p1": check_deep(0.1), "delta0": check_deep(0.0)}
results["transfer_tables"] = transfer_tables()
results["footings"] = footings()
results["meta"] = {"wall_s": round(time.time()-t_start, 3),
                   "rss_MB": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6, 2),
                   "grid_points": NGRID}

with open("AS017_outputs.json", "w") as f:
    json.dump(results, f, indent=1)

print(json.dumps({k: results[k] for k in ("constants", "footings", "meta")}, indent=1))
C1 = results["C1_transfer_identity"]
print("C1 max|resid_finite|", max(abs(x) for x in C1["resid_finite"]),
      " max|resid_linear|(O(q^2))", max(abs(x) for x in C1["resid_linear"]))
for tag in ("delta0p1", "delta0"):
    g = results["C2C3_gradient_decomp_"+tag]
    print(tag, "decomp", g["max_rel_resid_decomp"], "FD", g["max_rel_resid_FD"],
          "max|Delta/Sfull|", g["max_abs_Delta_over_Sfull"])
print("limits:", json.dumps(results["limits"], indent=1))
for tag in ("delta0p1", "delta0"):
    d = results["C4_deep_checks"][tag]
    print(tag, "flux", d["max_rel_flux_resid"], "exactrel", d["max_resid_exact_relation"],
          "devR1R2(deep y<=0.1)", d["max_dev_R1_R2_deep_domain"], "at y", d["y_at_max_dev"])
    print("  lead ratios:", d["lead_term_ratios"], " NT:", d["newtonian_tail"])
    print("  transfer:", json.dumps(d["transfer"], indent=1))
print("cluster:", json.dumps(results["transfer_tables"]["cluster"], indent=1))
print("wall_s", results["meta"]["wall_s"], "rss_MB", results["meta"]["rss_MB"])