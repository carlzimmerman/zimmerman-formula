#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG188 R2 -- (a) decoupling-limit kinetic coefficients, (b) FULL-theory local high-k scalar dispersion with the metric dynamical
(unitary gauge, uniform-acceleration background; DONE or NOT DONE is printed), (c) the tail bound (closed form, band and kernel sweep),
(d) Q2 by three recipes, EFE remark.
MUTATE=M1 (drop the monotonicity premise), M2 (band 99%), M10 (band applied to mu instead of g)."""
import sys, math
import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar, brentq
import CFG188_common as C

Q2 = C.Q2MAX

def R2a(chk, R):
    t, x, z, eps, g, F1, F2 = sp.symbols("t x z epsilon g F1 F2", real=True)
    ct, cx, cz, ctt, ctx_, ctz_, cxx, cxz, czz = sp.symbols("c_t c_x c_z c_tt c_tx c_tz c_xx c_xz c_zz", real=True)
    chi = ct * t + cx * x + cz * z + (ctt * t * t + 2 * ctx_ * t * x + 2 * ctz_ * t * z + cxx * x * x + 2 * cxz * x * z + czz * z * z) / 2   # 2nd-order jet of chi at the origin
    xs = [t, x, z]
    N = sp.exp(g * z)
    gm = sp.diag(-N ** 2, 1, 1); gi = gm.inv()
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(gm[d, b], xs[c]) + sp.diff(gm[d, c], xs[b]) - sp.diff(gm[b, c], xs[d])) for d in range(3)) / 2) for c in range(3)] for b in range(3)] for a in range(3)]
    phi = t + eps * chi
    dphi = [sp.diff(phi, v) for v in xs]
    X = sum(gi[a, a] * dphi[a] ** 2 for a in range(3))
    u_dn = [-dphi[a] / sp.sqrt(-X) for a in range(3)]
    u_up = [sum(gi[a, b] * u_dn[b] for b in range(3)) for a in range(3)]
    cov = [[sp.diff(u_dn[b], xs[a]) - sum(Gam[l][a][b] * u_dn[l] for l in range(3)) for b in range(3)] for a in range(3)]
    acc = [sum(u_up[a] * cov[a][b] for a in range(3)) for b in range(3)]
    a2 = sum(gi[a, a] * acc[a] ** 2 for a in range(3))
    a2 = a2.subs({t: 0, x: 0, z: 0})
    ser = sp.series(a2, eps, 0, 3).removeO()
    a20 = sp.simplify(ser.coeff(eps, 0)); d1 = ser.coeff(eps, 1); d2 = ser.coeff(eps, 2)
    print("  R2a: background a^2 =", a20)
    L2 = sp.expand(F1 * d2 + sp.Rational(1, 2) * F2 * d1 ** 2)      # sqrt(-g) = 1 at z = 0
    Kz = sp.simplify(L2.coeff(ctz_, 2)); Kx = sp.simplify(L2.coeff(ctx_, 2))
    print("  R2a: coefficient of (d_t d_z chi)^2 =", Kz, " ; of (d_t d_x chi)^2 =", Kx)
    y, astar = sp.symbols("y a_star", positive=True); q = sp.Function("q")
    sub = {F1: 2 * q(y), F2: sp.diff(q(y), y) / (astar * g)}
    Kz_y = sp.simplify(Kz.subs(sub).subs(g, y * astar)); Kx_y = sp.simplify(Kx.subs(sub).subs(g, y * astar))
    okz = sp.simplify(Kz_y - 2 * (q(y) + y * sp.diff(q(y), y))) == 0
    okx = sp.simplify(Kx_y - 2 * q(y)) == 0
    print("  R2a: K_z = 2 (y q)' ? ", okz, " ; K_x = 2 q ? ", okx)
    chk.add("R2.a: decoupling limit: radial kinetic coefficient of the flow = 2 (yq)', tangential = 2 q (sympy, generic q)", okz and okx)
    R["R2a_Kz"] = str(Kz_y); R["R2a_Kx"] = str(Kx_y)
    yv = np.array([0.1, 1.0, 2.0, 10.0])
    R["R2a_sign_table_P2"] = {str(v): [float(1 - 2 * v / math.sqrt(1 + 4 * v * v)), float(C.q_p2(v))] for v in yv}
    R["R2a_sign_table_exp"] = {str(v): [float((1 - v) * math.exp(-v)), float(math.exp(-v))] for v in yv}
    return okz and okx

def R2b(chk, R):
    """FULL scalar sector with the metric dynamical: N = e^{gz}(1+phi), N_i = d_i B, h_ij = e^{-2 psi} delta_ij, gauge E = 0 (unitary gauge, khronon = time).
    Lag = N sqrt(h) [K_ij K^ij - (1+c2) K^2 + R3 + F(a^2)],  a_i = d_i ln N.  Plane waves, averaged quadratic form, high-k (lambda^2) part."""
    th, eps, kx, kz, w, c2, g, F0, F1, F2, lam = sp.symbols("theta epsilon k_x k_z omega c2 g F0 F1 F2 lambda", real=True)
    A = sp.symbols("A1:7", real=True)
    phi = eps * (A[0] * sp.cos(th) + A[1] * sp.sin(th))
    psi = eps * (A[2] * sp.cos(th) + A[3] * sp.sin(th))
    B = eps * (A[4] * sp.cos(th) + A[5] * sp.sin(th))
    dth = lambda f, n=1: sp.diff(f, th, n)
    # derivatives: d_t -> -w d_theta, d_x -> kx d_theta, d_z -> kz d_theta
    psi_t = -w * dth(psi)
    kvec = [kx, 0, kz]
    Kij = sp.Matrix(3, 3, lambda i, j: -psi_t * (1 if i == j else 0) - kvec[i] * kvec[j] * dth(B, 2))
    KK = sum(Kij[i, j] ** 2 for i in range(3) for j in range(3))
    Ktr = sum(Kij[i, i] for i in range(3))
    k2 = kx ** 2 + kz ** 2
    lap_psi = k2 * dth(psi, 2); grad_psi2 = k2 * dth(psi) ** 2
    R3 = sp.exp(2 * psi) * (4 * lap_psi - 2 * grad_psi2)
    lnN_z = g + kz * dth(phi) / (1 + phi); lnN_x = kx * dth(phi) / (1 + phi)
    a2 = sp.exp(2 * psi) * (lnN_z ** 2 + lnN_x ** 2)
    da = a2 - g ** 2
    Fa = F0 + F1 * da + sp.Rational(1, 2) * F2 * da ** 2
    Lag = (1 + phi) * sp.exp(-3 * psi) * (KK - (1 + c2) * Ktr ** 2 + R3 + Fa)
    L2 = sp.series(Lag, eps, 0, 3).removeO().coeff(eps, 2)
    L2 = sp.expand(L2)
    Q = sp.integrate(L2, (th, 0, 2 * sp.pi)) / (2 * sp.pi)
    Q = sp.expand(sp.simplify(Q))
    # high-k scaling: k -> lam k, w -> lam w, and the shift amplitude B -> B/lam (d_i d_j B ~ psi); keep the lam^2 part of the quadratic form
    Qs = Q.subs({kx: lam * kx, kz: lam * kz, w: lam * w, A[4]: A[4] / lam, A[5]: A[5] / lam}, simultaneous=True)
    Qs = sp.expand(Qs)
    Q2p = sum(sp.expand(term).coeff(lam, 2) * lam ** 2 for term in [Qs]) / lam ** 2
    H2 = sp.hessian(sp.expand(Q2p), A)
    det = sp.factor(sp.simplify(H2.det()))
    print("  R2b: leading-order determinant of the (phi, psi, B) x (cos, sin) Hessian, factored:")
    print("      ", det)
    R["R2b_det"] = str(det)
    nondeg = det != 0
    kk = sp.sqrt(k2)
    kap = (F1 * k2 + 2 * F2 * g ** 2 * kz ** 2) / (2 * k2)
    w2_pred = c2 / (2 + 3 * c2) * k2 * (1 - kap) / kap
    W2 = sp.Symbol("W2")
    det_w2 = sp.simplify(det.subs(w, sp.sqrt(W2)))
    roots = sp.solve(sp.Eq(det_w2, 0), W2) if nondeg else []
    print("  R2b: roots omega^2 =", roots)
    ok = nondeg and any(sp.simplify(r_ - w2_pred) == 0 for r_ in roots)
    chk.add("R2.b (STRETCH, DONE): determinant non-degenerate and the full-theory local dispersion is omega^2 = c2/(2+3c2) k^2 (1-kappa)/kappa, kappa = (F1 + 2 F2 g^2 cos^2 alpha)/2 (sympy roots of det = 0)", ok, f"non-degenerate {nondeg}; roots {roots}")
    R["R2b_status"] = "DONE" if nondeg else "NOT DONE"
    R["R2b_dispersion"] = str(w2_pred)
    R["R2b_roots"] = [str(r_) for r_ in roots]
    # consequences
    ypq = lambda y_: 1 - 2 * y_ / math.sqrt(1 + 4 * y_ * y_)
    cs_rad = lambda y_, c2v: c2v / (2 + 3 * c2v) * (1 - ypq(y_)) / ypq(y_)
    R["R2b_cs2_radial_P2"] = {str(v): cs_rad(v, 1e-3) for v in (0.1, 1.0, 10.0, 1e3)}
    R["R2b_cs2_radial_exp"] = {str(v): 1e-3 / (2 + 3e-3) * (1 - (1 - v) * math.exp(-v)) / ((1 - v) * math.exp(-v)) for v in (0.5, 2.0, 5.0)}
    print("  R2b: radial c_s^2/c^2 at c2 = 1e-3: P2", R["R2b_cs2_radial_P2"], "; exponential kernel", R["R2b_cs2_radial_exp"])
    chk.add("R2.b: sign of the full-theory radial c_s^2 = sign((yq)'(1-(yq)')) for c2 > 0: P2 stable, exponential kernel unstable for y > 1", all(v > 0 for v in R["R2b_cs2_radial_P2"].values()) and all(v < 0 for k_, v in R["R2b_cs2_radial_exp"].items() if float(k_) > 1))
    return ok or okn

def tail_bound(target, band=0.10, ymax=None, ymin=None):
    eps = 1.0 - band
    gt = C.TARGETS[target]
    lo, hi = (ymin or 1e-6), (ymax or 1e6)
    f = lambda ly: -(eps * float(gt(math.exp(ly))) - math.exp(ly))
    ys = np.linspace(math.log(lo), math.log(hi), 4001)
    vals = np.array([-f(v) for v in ys])
    i = int(np.argmax(vals))
    res = minimize_scalar(f, bracket=(ys[max(i - 1, 0)], ys[i], ys[min(i + 1, len(ys) - 1)])) if 0 < i < len(ys) - 1 else None
    best = -res.fun if res is not None else vals[i]
    yN = math.exp(res.x) if res is not None else math.exp(ys[i])
    return best, yN

def mu_band_tail(band=0.10):
    """M10 wrong definition: the band is put on mu (i.e. on g_N/g at the same g) instead of on g at the same g_N."""
    ff = lambda y: -(y - (1 + band) * y * ((math.sqrt(1 + 4 * y * y) - 1) / (2 * y)))
    r = minimize_scalar(ff, bounds=(1e-3, 1e3), method="bounded")
    return -r.fun

def main():
    chk = C.Checks(); R = {}
    m = C.mode()
    print("CFG188 R2 -- stability, tail bound, Q2. mode:", m or "main")
    a0 = C.FOOT["canonical"]
    R_sat = 9.58 * C.AU        # Saturn semi-major axis, from memory (unverified); 9.54 AU used as sensitivity
    tol_tail = Q2 * R_sat / a0  # tail (in units of a0) at which g_ph/R hits the Q2 bound
    R["tail_tolerance_for_Q2"] = tol_tail
    if not m:
        R2a(chk, R)
        R2b(chk, R)
        # ---- R2.c closed form
        e = sp.symbols("epsilon", positive=True); y = sp.symbols("y", positive=True)
        Y = lambda zz: (-1 + sp.sqrt(1 + 4 * zz ** 2)) / 2
        s_lower = y - Y(y / e)
        ystar = sp.solve(sp.Eq(sp.diff(s_lower, y), 0), y)
        hcl = sp.simplify(s_lower.subs(y, ystar[0]))
        hclaim = (1 - sp.sqrt(1 - e ** 2)) / 2
        okcl = sp.simplify(hcl - hclaim) == 0 or all(abs(float((hcl - hclaim).subs(e, v))) < 1e-12 for v in (0.3, 0.5, 0.8, 0.9, 0.99))
        chk.add("R2.c: closed form h_min(eps) = (1 - sqrt(1-eps^2))/2 (sympy)", okcl, f"y* = {ystar}, h = {hcl}")
        R["closed_form"] = str(hcl)
        # sweeps
        table = {}
        for band in (0.01, 0.05, 0.10, 0.20, 0.30, 0.50, 0.80, 0.95, 0.98, 0.99):
            table[str(band)] = {"P2_closed": float((1 - math.sqrt(1 - (1 - band) ** 2)) / 2)}
        R["band_sweep_P2_closed_form"] = table
        for tgt in ("P2", "simple", "nu_mono"):
            v, yN = tail_bound(tgt, 0.10)
            vg, yNg = tail_bound(tgt, 0.10, ymin=1.1e-3, ymax=100.0)
            v20, _ = tail_bound(tgt, 0.20)
            v50, _ = tail_bound(tgt, 0.50)
            R[f"tail_{tgt}"] = {"band10": v, "at_yN": yN, "band10_restricted_to_G1_yN_range": vg, "yN_restricted": yNg, "band20": v20, "band50": v50}
            print(f"  R2c: {tgt}: minimal forced tail (band 10%) = {v:.5f} a0 at y_N* = {yN:.4f}; G1-range restricted {vg:.5f}; band 20% {v20:.5f}; band 50% {v50:.5f}")
        chk.add("R2.c: P2 tail 0.2821 (+-0.003)", abs(R["tail_P2"]["band10"] - 0.28206) < 0.003, f"{R['tail_P2']['band10']:.5f}")
        chk.add("R2.c: P2 20% band 0.2000 (+-0.001)", abs(R["tail_P2"]["band20"] - 0.2) < 0.001, f"{R['tail_P2']['band20']:.5f}")
        chk.add("R2.c: simple kernel 0.4675 (+-0.003)", abs(R["tail_simple"]["band10"] - 0.4675) < 0.003, f"{R['tail_simple']['band10']:.5f}")
        # band at which the bound reaches the Q2 tolerance
        f_b = lambda band: (1 - math.sqrt(1 - (1 - band) ** 2)) / 2 - tol_tail
        band_q2 = brentq(f_b, 0.5, 0.9999999)
        R["band_at_Q2_tolerance"] = band_q2
        print(f"  R2c: tail tolerance for Q2 = {tol_tail:.3e} a0; the +-band at which the closed-form bound reaches it = {100*band_q2:.2f}%")
        chk.add("R2.c: band at which the tail bound alone stops violating Q2 is ~98% (+-1%)", abs(band_q2 - 0.982) < 0.01, f"{100*band_q2:.2f}%")
        # (yq)'>=0 monotone premise: s(y) non-decreasing
        # ---- R2.d Q2 recipes
        out = {}
        for foot, a0si in C.FOOT.items():
            for Rname, Rm in (("Saturn9.58AU", 9.58 * C.AU), ("Saturn9.54AU", 9.54 * C.AU)):
                def gph(Rr):
                    yN = C.GM_SUN / Rr ** 2 / a0si
                    return a0si * (math.sqrt(yN * yN + yN) - yN)
                h_ = Rm * 1e-4
                dg = abs((gph(Rm + h_) - gph(Rm - h_)) / (2 * h_))
                tide = max(dg, gph(Rm) / Rm)
                out[f"{foot}_{Rname}_Sun_P2_tail"] = {"g_ph_over_a0": gph(Rm) / a0si, "tide": tide, "Q2_ratio": tide / Q2}
                tmin = R["tail_P2"]["band10"] * a0si / Rm
                out[f"{foot}_{Rname}_minimal_tail"] = {"tide": tmin, "Q2_ratio": tmin / Q2}
        R["Q2_recipeA"] = out
        rc = out["canonical_Saturn9.58AU_Sun_P2_tail"]["Q2_ratio"]; ra = out["alt_Saturn9.58AU_Sun_P2_tail"]["Q2_ratio"]; rm_ = out["canonical_Saturn9.58AU_minimal_tail"]["Q2_ratio"]
        print(f"  R2d recipe A (tide = max(|dg/dR|, g/R), Saturn 9.58 AU): Sun's own P2 tail canonical {rc:.3e}, alt {ra:.3e}; minimal tail {rm_:.3e} (9.54 AU: {out['canonical_Saturn9.54AU_Sun_P2_tail']['Q2_ratio']:.3e})")
        chk.add("R2.d: Q2 canonical 6.3e3 (+-10% frozen D-2 line; sensitivity to Saturn distance reported)", abs(out["canonical_Saturn9.54AU_Sun_P2_tail"]["Q2_ratio"] / 6.3e3 - 1) < 0.05 and abs(rc / 6.3e3 - 1) < 0.10, f"{rc:.3e} / 9.54 AU {out['canonical_Saturn9.54AU_Sun_P2_tail']['Q2_ratio']:.3e}")
        chk.add("R2.d: Q2 alt footing 7.6e3 (+-10%)", abs(ra / 7.6e3 - 1) < 0.10, f"{ra:.3e}")
        chk.add("R2.d: minimal-tail Q2 3.6e3 (+-10%)", abs(rm_ / 3.6e3 - 1) < 0.10, f"{rm_:.3e}")
        # recipe B: apsidal precession of a near-circular orbit with constant radial extra acceleration eps: 2 pi eps / g_N per orbit
        recB = {}
        for body, Rr_au, Tyr in (("Earth", 1.0, 1.0), ("Mars", 1.524, 1.881), ("Saturn", 9.58, 29.457)):
            Rr = Rr_au * C.AU; gN = C.GM_SUN / Rr ** 2
            for label, epsx in (("Sun_P2_tail_0.5a0", 0.5 * a0), ("minimal_tail_0.282a0", R["tail_P2"]["band10"] * a0)):
                dphi = 2 * math.pi * epsx / gN                                       # rad per orbit
                arcsec_cy = dphi * (100.0 / Tyr) * 206264.806
                recB[f"{body}_{label}"] = {"rad_per_orbit": dphi, "arcsec_per_century": arcsec_cy}
        R["Q2_recipeB_precession"] = recB
        print("  R2d recipe B (apsidal precession 2 pi eps/g_N per orbit, near-circular; hand formula): Saturn, minimal tail:", f"{recB['Saturn_minimal_tail_0.282a0']['arcsec_per_century']:.2f} arcsec/century; Earth: {recB['Earth_minimal_tail_0.282a0']['arcsec_per_century']:.3f} arcsec/century")
        print("      (ephemeris precession bounds are NOT stated by me: no reliable number from memory -> ratio NOT SCORED for recipe B)")
        # recipe C: direct anomalous acceleration vs quoted delta A_R bounds at Earth/Mars
        recC = {"Earth": R["tail_P2"]["band10"] * a0 / 3.66e-14, "Mars": R["tail_P2"]["band10"] * a0 / 3.72e-14}
        R["Q2_recipeC_minimal_tail_over_dAR_bound"] = recC
        print(f"  R2d recipe C (0.282 a0 vs the quoted delta A_R bounds 3.66e-14 / 3.72e-14 m/s^2): Earth {recC['Earth']:.3e}, Mars {recC['Mars']:.3e}")
        chk.add("R2.d: 'pincer survives' line: recipes A and C give ratio >= 100 for the minimal tail (recipe B not scored)", rm_ >= 100 and min(recC.values()) >= 100)
        # EFE remark (first order in g_e/g_N): dipole only
        xx, yy, zz, ge, kN = sp.symbols("x y z g_e k", positive=True)
        rr = sp.sqrt(xx ** 2 + yy ** 2 + zz ** 2)
        vx, vy, vz = -kN * xx / rr ** 3, -kN * yy / rr ** 3, -kN * zz / rr ** 3 + ge
        vn = sp.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
        nx, ny, nz = vx / vn, vy / vn, vz / vn
        div = sp.diff(nx, xx) + sp.diff(ny, yy) + sp.diff(nz, zz)
        d1 = sp.simplify(sp.diff(div, ge).subs(ge, 0))
        print("  EFE remark: first-order (g_e) change of div n_hat =", d1)
        R["EFE_first_order_div_change"] = str(d1)
        chk.add("EFE remark (diagnostic): the first-order external-field change of the phantom source div(n_hat) is a pure dipole (odd in z), so the monopole a0/2 tail is unchanged at first order", sp.simplify(d1.subs(zz, -zz) + d1) == 0, str(d1))
    # ------------------------------------------------------------ MUTATE
    bit = None; ok = None
    if m == "M1":
        # premise dropped: s(y) may decrease.  The minimal admissible s is max(0, lower band edge); tail at y = 1e6 -> 0
        eps_ = 0.9
        Yf = lambda zz: (-1 + math.sqrt(1 + 4 * zz * zz)) / 2
        s_min = lambda yv: max(0.0, yv - Yf(yv / eps_))
        tail_hi = s_min(1e6); s_peak = max(s_min(v) for v in np.linspace(0.2, 3, 300))
        R["M1_tail_at_1e6"] = tail_hi; R["M1_peak_s"] = s_peak
        bit = "the tail lower bound (>= 0.2 a0) holds with the monotonicity premise dropped"; ok = tail_hi < 1e-4
        print(f"  M1: with (yq)' >= 0 dropped the forced tail at y = 1e6 is {tail_hi:.2e} a0 (peak of the lower edge {s_peak:.3f}); an s(y) that rises to {s_peak:.3f} and falls to 0 has (yq)' < 0 somewhere")
    elif m == "M2":
        band = 0.99
        h = (1 - math.sqrt(1 - (1 - band) ** 2)) / 2
        R["M2_tail_bound"] = h; R["M2_tolerance"] = tol_tail
        bit = "the tail lower bound exceeds the Q2 tolerance"; ok = h < tol_tail
        print(f"  M2: band 99%: forced tail >= {h:.3e} a0 versus tolerance {tol_tail:.3e} a0")
    elif m == "M10":
        v = mu_band_tail(0.10)
        R["M10_tail_mu_band"] = v
        bit = "the tail bound is definition-robust (band on mu gives the same 0.282 within 5%)"; ok = abs(v / 0.28206 - 1) > 0.05
        print(f"  M10: band placed on mu instead of g gives {v:.4f} a0 (versus 0.2821): differs by {100*(v/0.28206-1):.1f}%")
    C.finish(__file__, chk, R, bit, ok)

if __name__ == "__main__":
    C.guarded(main)
